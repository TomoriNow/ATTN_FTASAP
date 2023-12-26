from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from main.forms import CustomUserCreationForm, CustomUserCreationForm2
#from main.forms import  AccountUserCreation, StaffUserCreation, ChildUserCreation,
#from main.models import AccountUser
from django.contrib import messages
import uuid
import psycopg2
from main.config import config
import datetime
from django.core.paginator import Paginator

def show_main(request):
    return render(request, 'main.html', {})

def register(request):
    return render(request, 'register.html', {})

def login_user(request):
    if request.method == 'POST':
        phoneNo = request.POST.get('phoneNo')
        password = request.POST.get('password')
        user = authenticate(request, username=phoneNo, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse("main:dashboard"))
            else:
                
                try:
                    params = config()
                    connection = psycopg2.connect(**params)

                    # create a cursor
                    crsr = connection.cursor()
                    # sql command to be executed for fetching the data
                    sqlStr = "select * from u"

                    # execute the data fetch SQL command along with the SQL placeholder values
                    crsr.execute("select * from u where phonenumber = %s", (request.POST["phoneNo"],))
                    user = crsr.fetchone()
                    userid= str(user[0])
                    request.session["userid"] = userid
                    request.session["phoneNo"] = str(user[2])
                    request.session["name"] = str(user[3]) + " " + str(user[4])
                    request.session["gender"] = str(user[5])
                    request.session["birthDate"] = str(user[6])
                    request.session["address"] = str(user[7])
                    if not request.user.is_staff:
                        crsr.execute("select * from child where userid = %s", (userid,))
                        child = crsr.fetchone()
                        request.session["dadName"] = child[1]
                        request.session["momName"] = child[2]
                        request.session["dadJob"] = child[3]
                        request.session["momJob"] = child[4]
                    else:
                        request.session["is_driver"] = False
                        request.session["is_caregiver"] = False
                        crsr.execute("select * from staff where userid = %s", (userid,))
                        staff = crsr.fetchone()
                        request.session["NIK"] = staff[1]
                        request.session["NPWP"] = staff[2]
                        request.session["bankAccount"] = staff[3]
                        request.session["bankName"] = staff[4]
                        crsr.execute("select * from caregiver where userid = %s", (userid,))
                        caregiver = crsr.fetchone()
                        if caregiver is not None:
                            request.session["is_caregiver"] = True
                            crsr.execute("select * from caregiver_certificate where userid = %s", (userid,))
                            certificates = crsr.fetchall()
                            request.session["certificates"] = [(i[2], i[1], i[3], i[4]) for i in certificates]
                        else:
                            request.session["is_driver"] = True
                            crsr.execute("select * from driver where userid = %s", (userid,))
                            driver = crsr.fetchone()
                            request.session["driverNo"] = driver[1]
                            crsr.execute("select * from driver_day where userid = %s", (userid,))
                            days = crsr.fetchall()
                            request.session["driverDays"] = [i[1] for i in days]
                    crsr.close()
                except(Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if connection is not None:
                        connection.close()
            return HttpResponseRedirect(reverse("main:dashboard"))
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login_user'))
    response.delete_cookie('last_login')
    return redirect('main:login_user')

def register_admin(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True  # Set the user as a superuser
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('main:dashboard')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'register_admin.html', context)

def register_staff(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
#        form2 = AccountUserCreation(request.POST)
#        form3 = StaffUserCreation(request.POST)
        
        if form.is_valid():# and form2.is_valid() and form3.is_valid():
            user = form.save(commit=False)
            user.is_staff=True
            user.save()
#            account = form2.save(commit=False)
#            account.user=user
#            account.is_staff=True
#            account.save()
#            staff = form3.save(commit=False)
#            staff.user = account
#            staff.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login_user')
    else:
        form = CustomUserCreationForm()
#        form2 = AccountUserCreation()
#        form3 = StaffUserCreation()

    context = {'form': form}# 'form2':form2, 'form3':form3}
    return render(request, 'register_staff.html', context)

def register_child(request):
    if request.method == "POST":
        form = CustomUserCreationForm2(request.POST)
        
        if form.is_valid():# and form2.is_valid() and form3.is_valid():
            connection = None
            try:
                params = config()
                connection = psycopg2.connect(**params)

                # create a cursor
                crsr = connection.cursor()
                # sql command to be executed for fetching the data
                sqlStr = "insert into u VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                userId = uuid.uuid4()

                # execute the data fetch SQL command along with the SQL placeholder values
                crsr.execute("insert into u VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (userId, 
                    request.POST['password1'], request.POST['username'], request.POST['firstName'], 
                    request.POST['lastName'], request.POST['gender'], request.POST['birthDate'], request.POST['address']))
                crsr.execute("insert into child VALUES (%s, %s, %s, %s, %s)", (userId, request.POST['dadName'], 
                    request.POST['momName'], request.POST['dadJob'], request.POST['momJob']))
                connection.commit()
                crsr.close()
                user = form.save(commit=False)
                user.save()
            except(Exception, psycopg2.DatabaseError) as error:
                messages.info(request, error.diag.message_primary)
                form = CustomUserCreationForm2()

                context = {'form': form}
                return render(request, 'register_child.html', context)
            finally:
                if connection is not None:
                    connection.close()
            login(request, user)
            request.session["userid"] = str(userId)
            request.session["phoneNo"] = request.POST['username']
            request.session["name"] = str(request.POST['firstName']) + " " + str(request.POST['lastName'])
            request.session["gender"] = str(request.POST['gender'])
            request.session["birthDate"] = str(request.POST['birthDate'])
            request.session["address"] = str(request.POST['address'])
            request.session["dadName"] = str(request.POST['dadName'])
            request.session["momName"] = str(request.POST['momName'])
            request.session["dadJob"] = str(request.POST['dadJob'])
            request.session["momJob"] = str(request.POST['momJob'])
            return redirect('main:dashboard')
        else:
            messages.info(request, 'Invalid password or phone number')
    else:
        form = CustomUserCreationForm2()

    context = {'form': form}
    return render(request, 'register_child.html', context)

def dashboard(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'admin_dashboard.html', {})
    if not user.is_staff:
        return render(request, 'child_dashboard.html', {})
    if request.session["is_caregiver"]:
        return render(request, 'caregiver_dashboard.html', {})
    else:
        return render(request, 'driver_dashboard.html', {})
    #account = AccountUser.objects.get(user = request.user)
    #if account.is_child:
    #    return render(request, 'child_dashboard.html', {})
    #if account.is_staff:
    #    return render(request, 'driver_dashboard.html', {})

def register_driver(request):
    if request.method == "POST":
        form = CustomUserCreationForm2(request.POST)
        if form.is_valid():# and form2.is_valid() and form3.is_valid():
            connection = None
            try:
                params = config()
                connection = psycopg2.connect(**params)

                # create a cursor
                crsr = connection.cursor()
                # sql command to be executed for fetching the data
                sqlStr = "insert into u VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                userId = uuid.uuid4()

                # execute the data fetch SQL command along with the SQL placeholder values
                crsr.execute("insert into u VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (userId, 
                    request.POST['password1'], request.POST['username'], request.POST['firstName'], 
                    request.POST['lastName'], request.POST['gender'], request.POST['birthDate'], request.POST['address']))
                crsr.execute("insert into staff VALUES (%s, %s, %s, %s, %s)", (userId, request.POST['NIK'], 
                    request.POST['NPWP'], request.POST['BankAccount'], request.POST['BankName']))
                crsr.execute("insert into driver VALUES (%s, %s)", (userId, request.POST['drivingLicense'],))
                pyargs = [(userId, i) for i in request.POST.getlist('day')]
                args = ','.join(crsr.mogrify("(%s,%s)", i).decode('utf-8')
                for i in pyargs)
                crsr.execute("insert into driver_day VALUES " + (args))

                connection.commit()
                crsr.close()
                user = form.save(commit=False)
                user.is_staff = True
                user.save()
            except(Exception, psycopg2.DatabaseError) as error:
                messages.info(request, error.diag.message_primary)
                form = CustomUserCreationForm()
                context = {'form': form}
                return render(request, 'register_driver.html', context)
            finally:
                if connection is not None:
                    connection.close()
            login(request, user)
            request.session["userid"] = str(userId)
            request.session["phoneNo"] = request.POST['username']
            request.session["name"] = str(request.POST['firstName']) + " " + str(request.POST['lastName'])
            request.session["gender"] = str(request.POST['gender'])
            request.session["birthDate"] = str(request.POST['birthDate'])
            request.session["address"] = str(request.POST['address'])
            request.session["NIK"] = request.POST['NIK']
            request.session["NPWP"] = request.POST['NPWP']
            request.session["bankAccount"] = request.POST['BankAccount']
            request.session["bankName"] = request.POST['BankName']
            request.session["is_driver"] = True
            request.session["is_caregiver"] = False
            request.session["driverNo"] = request.POST['drivingLicense']
            request.session["driverDays"] = request.POST.getlist('day')
            return redirect('main:dashboard')
    else:
        form = CustomUserCreationForm()
#        form2 = AccountUserCreation()
#        form3 = StaffUserCreation()
    context = {'form': form}# 'form2':form2, 'form3':form3}
    return render(request, 'register_driver.html', context)

def register_caregiver(request):
    if request.method == "POST":
        form = CustomUserCreationForm2(request.POST)
        if form.is_valid():# and form2.is_valid() and form3.is_valid():
            connection = None
            try:
                params = config()
                connection = psycopg2.connect(**params)

                # create a cursor
                crsr = connection.cursor()
                # sql command to be executed for fetching the data
                sqlStr = "insert into u VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                userId = uuid.uuid4()

                # execute the data fetch SQL command along with the SQL placeholder values
                crsr.execute("insert into u VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (userId, 
                    request.POST['password1'], request.POST['username'], request.POST['firstName'], 
                    request.POST['lastName'], request.POST['gender'], request.POST['birthDate'], request.POST['address']))
                crsr.execute("insert into staff VALUES (%s, %s, %s, %s, %s)", (userId, request.POST['NIK'], 
                    request.POST['NPWP'], request.POST['BankAccount'], request.POST['BankName']))
                crsr.execute("insert into caregiver VALUES (%s)", (userId,))

                pyargs = [(userId, a, b, c, d) for a, b, c, d in zip(request.POST.getlist('certNumber'), request.POST.getlist('certName'), 
                        request.POST.getlist('certYear'), request.POST.getlist('certOrganizer'))]
                args = ','.join(crsr.mogrify("(%s,%s,%s,%s,%s)", i).decode('utf-8')
                for i in pyargs)
                crsr.execute("insert into caregiver_certificate VALUES " + (args))

                connection.commit()
                crsr.close()
                user = form.save(commit=False)
                user.is_staff = True
                user.save()
            except(Exception, psycopg2.DatabaseError) as error:
                messages.info(request, error.diag.message_primary)
                form = CustomUserCreationForm()
                context = {'form': form}
                return render(request, 'register_caregiver.html', context)
            finally:
                if connection is not None:
                    connection.close()
            
            login(request, user)
            request.session["userid"] = str(userId)
            request.session["phoneNo"] = request.POST['username']
            request.session["name"] = str(request.POST['firstName']) + " " + str(request.POST['lastName'])
            request.session["gender"] = str(request.POST['gender'])
            request.session["birthDate"] = str(request.POST['birthDate'])
            request.session["address"] = str(request.POST['address'])
            request.session["NIK"] = request.POST['NIK']
            request.session["NPWP"] = request.POST['NPWP']
            request.session["bankAccount"] = request.POST['BankAccount']
            request.session["bankName"] = request.POST['BankName']
            request.session["is_driver"] = False
            request.session["is_caregiver"] = True
            request.session["certificates"] = [(a, b, c, d) for a, b, c, d in zip(request.POST.getlist('certName'), request.POST.getlist('certNumber'), 
                        request.POST.getlist('certYear'), request.POST.getlist('certOrganizer'))]
            return redirect('main:dashboard')
    else:
        form = CustomUserCreationForm()
#        form2 = AccountUserCreation()
#        form3 = StaffUserCreation()
    context = {'form': form}# 'form2':form2, 'form3':form3}
    return render(request, 'register_caregiver.html', {})

def daily_report_child(request):
    return render(request, 'daily_report_child.html', {})

def child_list(request):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT U.firstname, U.lastname, DATE_PART('YEAR', AGE(CURRENT_DATE, U.birthdate)) as age, TO_CHAR(U.birthdate, 'Month') as month, EXTRACT(DAY FROM U.birthdate) as day, t.class, U.phonenumber
        FROM U, (
            SELECT
            C.userid, E.year, E.class, 
            ROW_NUMBER() OVER (PARTITION BY C.userid 
            ORDER BY year DESC) AS row_number
            FROM Child C LEFT OUTER JOIN Enrollment E ON C.userid = E.userid
        ) t
        WHERE t.row_number = 1 AND U.userid = t.userid;
        """

        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlStr)
        result = crsr.fetchall()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return render(request, 'child_list.html', {'result': result})

def new_activity_schedule(request, id, name, year):
    context = {'id': id, 'name': name, 'year': year}
    if request.method == "POST":
        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()

            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute("insert into activity_schedule VALUES (%s, %s, %s, %s, %s, %s)", (id, 
                year, request.POST['day'], request.POST['startHour'], 
                request.POST['endHour'], request.POST['activity']))
            connection.commit()
            crsr.close()
            return redirect('main:offered_program_detail', id= id,name = name, year = year)
        except(Exception, psycopg2.DatabaseError) as error:
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT * from activity
        """
        crsr.execute(sqlStr)
        activities = crsr.fetchall()
        context['activities'] = activities
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return render(request, 'new_activity_schedule.html', context)

def new_menu_schedule(request, id, name, year):
    context = {'id': id, 'name': name, 'year': year}
    if request.method == "POST":
        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()

            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute("insert into menu_schedule VALUES (%s, %s, %s, %s, %s), (%s, %s, %s, %s, %s), (%s, %s, %s, %s, %s)", (id, 
                year, request.POST['day'], request.POST['morningSnackHour'], request.POST['morningSnack'], id, year, 
                request.POST['day'], request.POST['lunchHour'], request.POST['lunch'], id, year, request.POST['day'],
                request.POST['afternoonSnackHour'], request.POST['afternoonSnack']))
            connection.commit()
            crsr.close()
            return redirect('main:offered_program_detail', id= id,name = name, year = year)
        except(Exception, psycopg2.DatabaseError) as error:
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT * from menu
        """
        crsr.execute(sqlStr)
        menus = crsr.fetchall()
        context['menus'] = menus
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return render(request, 'new_menu_schedule.html', context)

def new_offered_program(request):
    today = datetime.datetime.now()

    #accessing the year attribute
    year = today.year
    if request.method == "POST":
        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()

            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute("insert into offered_program VALUES (%s, %s, %s, %s)", (request.POST['program'], 
                year, request.POST['monthlyFee'], request.POST['dailyFee']))
            connection.commit()
            crsr.close()
            return redirect('main:offered_program')
        except(Exception, psycopg2.DatabaseError) as error:
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT * from program
        WHERE programid NOT IN
        (SELECT programid from offered_program where year = %s)
        """
        crsr.execute(sqlStr, (year,))
        programs = crsr.fetchall()
        print(programs)
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return render(request, 'new_offered_program.html', {'programs': programs})

def offered_program_detail(request, id, name, year):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT A.name, S.day , S.starthour, S.endhour
        FROM Activity_schedule S, Activity A
        WHERE S.activityid = A.id AND S.programid = %s AND S.year = %s
        ORDER BY A.name;
        """
        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlStr, (id, year,))
        activities = crsr.fetchall()
        sqlStr = """
        SELECT M.name, S.day , S.hour
        FROM Menu_schedule S, Menu M
        WHERE S.menuid = M.id AND S.programid = %s AND S.year = %s
        ORDER BY S.day;
        """
        crsr.execute(sqlStr, (id, year,))
        menus = crsr.fetchall()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return render(request, 'offered_program_detail.html', {'activities': activities, 'menus': menus, 'id': id, 'name': name, 'year': year})

def offered_program(request):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT P.programid, P.name , O.year, O.monthlyfee, O.dailyfee, NOT EXISTS(SELECT * FROM class where (programid,year) = (P.programid, O.year))
        FROM Offered_program O, Program P
        WHERE O.programid = P.programid
        ORDER BY year DESC, P.name;
        """

        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlStr)
        result = crsr.fetchall()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return render(request, 'offered_program.html', {'result': result})

def delete_offered_program(request, id, year):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()

        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute("delete from offered_program where programid = %s and year = %s", (id, year,))
        connection.commit()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        messages.info(request, error.diag.message_primary)
    finally:
        if connection is not None:
            connection.close()
    return HttpResponseRedirect(reverse('main:offered_program'))


def crud_extracurricular(request):
    if request.user.is_superuser:
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            # sql command to be executed for fetching the data
            sqlStr = """
            SELECT EX.extracurricularid, EX.name, EX.day, EX.hour, NOT EXISTS(SELECT * FROM extracurricular_taking ET where ET.extracurricularid=EX.extracurricularid)
            FROM extracurricular EX
            ORDER BY EX.name ASC;
            """
            
            crsr.execute(sqlStr)
            result = crsr.fetchall()
            crsr.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    return render(request, 'crud_extracurricular.html', {'result':result})
    
def delete_activity(request, id):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        
        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute("delete from activity where id=%s;", (id,))
        connection.commit()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print("something")
        print(error)
        messages.info(request, error.diag.message_primary)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
    return HttpResponseRedirect(reverse('main:activity'))

def activity(request):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        
        sqlStr = """
        select DISTINCT a.id, a.name, NOT EXISTS(SELECT * FROM ACTIVITY where (id) =  AC.Activityid) AS yes
from activity A 
LEFT JOIN ACTIVITY_SCHEDULE AC ON ac.activityid = a.id
order by yes;
        """
        
        crsr.execute(sqlStr)
        result = crsr.fetchall()
        print(result)
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
    return render(request, 'activity.html', {'result':result})

def extracurricular_detail(request, id, name, day, hour):
    if request.user.is_superuser:
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            # sql command to be executed for fetching the data
            sqlStr = """
            SELECT U.firstname, U.lastname, ET.class
            FROM U, extracurricular_taking ET
            WHERE ET.extracurricularid = %s AND U.userid = ET.userid
            """
            
            crsr.execute(sqlStr, (id,))
            participant = crsr.fetchall()
            crsr.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    return render(request, 'extracurricular_detail.html', {'participant':participant, 'id':id, 'name':name, 'day':day, 'hour':hour})

def delete_extracurricular(request, id):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        
        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute("delete from extracurricular where extracurricularid=%s", (id,))
        connection.commit()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print("something")
        print(error)
        messages.info(request, error.diag.message_primary)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
    return HttpResponseRedirect(reverse('main:crud_extracurricular'))

def add_extracurricular(request):
    if request.method=="POST":
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            sqlStr = """
            INSERT into extracurricular VALUES (%s, %s, %s, %s);
            """
            extracurricularID = uuid.uuid4()
            
            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute(sqlStr, (extracurricularID, request.POST['extracurricularName'], request.POST['extracurricularDay'], 
                request.POST['extracurricularHour'],))
            connection.commit()
            crsr.close()
            return redirect('main:crud_extracurricular')
        except(Exception, psycopg2.DatabaseError) as error:
            print("something")
            print(error)
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    
    return render(request, 'extracurricular_form.html', {})

def add_activity(request):
    if request.method=="POST":
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            sqlStr = """
            INSERT into extracurricular VALUES (%s, %s);
            """
            extracurricularID = uuid.uuid4()
            
            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute(sqlStr, (extracurricularID, request.POST['CreateActivity'],))
            connection.commit()
            crsr.close()
            return redirect('main:activity.html')
        except(Exception, psycopg2.DatabaseError) as error:
            print("something")
            print(error)
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    
    return render(request, 'create_activity.html', {})

def update_extracurricular(request, id, name, day, hour):
    if request.method=="POST":
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            sqlStr = """
            UPDATE extracurricular
            SET name = %s, day = %s, hour = %s
            WHERE extracurricularid=%s;
            """
            
            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute(sqlStr, (request.POST['extracurricularName'], request.POST['extracurricularDay'], 
                request.POST['extracurricularHour'], id,))
            connection.commit()
            crsr.close()
            return redirect('main:crud_extracurricular')
        except(Exception, psycopg2.DatabaseError) as error:
            print("something")
            print(error)
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    
    return render(request, 'update_extracurricular.html', {'id': id, 'name':name, 'day':day, 'hour':hour})
    
def child_payment(request):
    expectedMonthly = 0
    expectedDaily = 0
    expectedFine = 0
    
    if request.method == "POST":
        connection=None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)
            crsr = connection.cursor()
            userid = request.session['userid']
            
            sqlStrProgramID ="""
            SELECT E.programid
            FROM enrollment E
            WHERE E.userid = %s;
            """
            crsr.execute(sqlStrProgramID, (userid,))
            programid = crsr.fetchone()
            
            sqlStrYear="""
            SELECT E.year
            FROM enrollment E
            WHERE E.userid = %s;
            """
            crsr.execute(sqlStrYear, (userid,))
            year = crsr.fetchone()
            
            sqlStrClass="""
            SELECT E.class
            FROM enrollment E
            WHERE E.userid = %s;
            """
            crsr.execute(sqlStrClass, (userid,))
            e_class = crsr.fetchone()
            
            sqlStrExpectedFine="""
            SELECT PH.fine
            FROM payment_history PH
            WHERE PH.userid=%s; 
            """
            crsr.execute(sqlStrExpectedFine, (userid,))
            expectedFine = crsr.fetchone()
            
            if expectedFine is not None and expectedFine[0] is not None:
                expectedFine = int(expectedFine[0])
            else:
                expectedFine = 0
            
            sqlStrExpectedMonthly="""
            SELECT O.monthlyfee
            FROM offered_program O
            WHERE O.programid = %s AND O.year = %s;
            """
            crsr.execute(sqlStrExpectedMonthly, (programid, year,))
            expectedMonthly = crsr.fetchone()
            
            if expectedMonthly is not None and expectedMonthly[0] is not None:
                expectedMonthly = int(expectedMonthly[0])
            else:
                expectedMonthly = 0
            
            sqlStrExpectedDaily="""
            SELECT O.dailyfee
            FROM offered_program O
            WHERE O.programid = %s AND O.year = %s;
            """
            crsr.execute(sqlStrExpectedDaily, (programid, year,))
            expectedDaily = crsr.fetchone()
            
            if expectedDaily is not None and expectedDaily[0] is not None:
                expectedDaily = int(expectedDaily[0])
            else:
                expectedDaily = 0
            
            sqlStr = """
            INSERT INTO PAYMENT_HISTORY
            VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, %s)
            """
            paymentID = uuid.uuid4()
            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute(sqlStr, (paymentID, userid, programid, year, e_class, request.POST['paymentDate'], request.POST['paymentType'], request.POST['paymentAmount'],))
            connection.commit()
            crsr.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)
        crsr = connection.cursor()
        userid = request.session['userid']
        
        sqlStrProgramID ="""
        SELECT E.programid
        FROM enrollment E
        WHERE E.userid = %s;
        """
        crsr.execute(sqlStrProgramID, (userid,))
        programid = crsr.fetchone()
        
        sqlStrYear="""
        SELECT E.year
        FROM enrollment E
        WHERE E.userid = %s;
        """
        crsr.execute(sqlStrYear, (userid,))
        year = crsr.fetchone()
        
        sqlStrClass="""
        SELECT E.class
        FROM enrollment E
        WHERE E.userid = %s;
        """
        crsr.execute(sqlStrClass, (userid,))
        e_class = crsr.fetchone()
        
        sqlStrExpectedFine="""
        SELECT PH.fine
        FROM payment_history PH
        WHERE PH.userid=%s; 
        """
        crsr.execute(sqlStrExpectedFine, (userid,))
        expectedFine = crsr.fetchone()
        
        if expectedFine is not None and expectedFine[0] is not None:
            expectedFine = int(expectedFine[0])
        else:
            expectedFine = 0
            
        print(expectedFine)
        
        sqlStrExpectedMonthly="""
        SELECT O.monthlyfee
        FROM offered_program O
        WHERE O.programid = %s AND O.year = %s;
        """
        crsr.execute(sqlStrExpectedMonthly, (programid, year,))
        expectedMonthly = crsr.fetchone()
        
        if expectedMonthly is not None and expectedMonthly[0] is not None:
            expectedMonthly = int(expectedMonthly[0])
        else:
            expectedMonthly = 0
        
        print(expectedMonthly)
        
        sqlStrExpectedDaily="""
        SELECT O.dailyfee
        FROM offered_program O
        WHERE O.programid = %s AND O.year = %s;
        """
        crsr.execute(sqlStrExpectedDaily, (programid, year,))
        expectedDaily = crsr.fetchone()
        
        if expectedDaily is not None and expectedDaily[0] is not None:
            expectedDaily = int(expectedDaily[0])
        else:
            expectedDaily = 0
        
        print(expectedDaily)
        
        crsr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
    
    return render(request, 'child_payment.html', {'expectedFine': expectedFine, 'expectedMonthly': expectedMonthly, 'expectedDaily': expectedDaily})

def payment_history(request):
    
    if request.user.is_superuser:
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            # sql command to be executed for fetching the data
            sqlStr = """
            SELECT U.firstname, U.lastname, PH.paymentdate, PH.type, PH.fine, PH.amount
            FROM U, payment_history PH, program P
            WHERE U.userid=PH.userid AND P.programid=PH.programid
            ORDER BY PH.paymentdate DESC;
            """
            
            crsr.execute(sqlStr)
            result = crsr.fetchall()
            crsr.close()
            
            p = Paginator(result, 20)
            page = request.GET.get('page')
            payments = p.get_page(page)
            
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    else:
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            # sql command to be executed for fetching the data
            sqlStr = """
            SELECT DISTINCT P.name, E.year, E.class, PH.paymentdate, PH.type, PH.fine, PH.amount
            FROM Enrollment E, payment_history PH, Program P
            WHERE P.programid=PH.programid AND E.programid=PH.programid AND E.class=PH.class AND E.year=PH.year AND PH.userid=%s;
            """
            
            crsr.execute(sqlStr, (request.session['userid'],))
            result = crsr.fetchall()
            crsr.close()
            
            p = Paginator(result, 20)
            page = request.GET.get('page')
            payments = p.get_page(page)
            
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')

    return render(request, 'payment_history.html', {'result':result, 'payments':payments})

def create_activity(request):
    if request.method=="POST":
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            sqlStr = """
            INSERT into activity VALUES (%s, %s);
            """
            extracurricularID = uuid.uuid4()
            
            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute(sqlStr, (extracurricularID, request.POST['CreateActivity'],))
            connection.commit()
            crsr.close()
            return redirect('main:activity')
        except(Exception, psycopg2.DatabaseError) as error:
            print("something")
            print(error)
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    
    return render(request, 'create_activity.html', {})

def edit_activity(request, id, name):
    if request.method=="POST":
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            sqlStr = """
            UPDATE activity
            SET name = %s
            WHERE id=%s;
            """
            
            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute(sqlStr, (request.POST['EditActivity'], id,))
            connection.commit()
            crsr.close()
            return redirect('main:activity')
        except(Exception, psycopg2.DatabaseError) as error:
            print("something")
            print(error)
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    
    return render(request, 'edit_activity.html', {'id': id, 'name':name})

def display_dad_name(request, dadName):
    # You can use dadName in the template or perform any other logic
    context = {'dadName': dadName}
    return render(request, 'display_dad_name.html', context)
        
def caregiver_dashboard(request):
    return render(request, 'caregiver_dashboard.html', {})

def driver_dashboard(request):
    return render(request, 'driver_dashboard.html', {})

def create_room(request):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT r.roomno, r.area
        from room r;
        """

        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlStr)
        result = crsr.fetchall()
        print(result)
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')        
    return render(request, 'create_room.html', {'result': result})

def manage_menu(request):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT m.name, m.type
        from menu m;
        """

        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlStr)
        result = crsr.fetchall()
        print(result)
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')        
    return render(request, 'manage_menu.html', {'result': result})

def menu_form(request):
    if request.method=="POST":
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            sqlStr = """
            INSERT into menu VALUES (%s, %s, %s);
            """
            menuID = uuid.uuid4()
            
            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute(sqlStr, (menuID, request.POST['MenuName'], request.POST['MenuType']))
            connection.commit()
            crsr.close()
            return redirect('main:activity.html')
        except(Exception, psycopg2.DatabaseError) as error:
            print("something")
            print(error)
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    return render(request, 'menu_form.html', {})

def room_form(request):
    if request.method=="POST":
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            sqlStr = """
            INSERT into menu VALUES (%s, %s, %s);
            """
            roomID = uuid.uuid4()
            
            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute(sqlStr, (roomID, request.POST['Roomnumber'], request.POST['Area']))
            connection.commit()
            crsr.close()
            return redirect('main:activity.html')
        except(Exception, psycopg2.DatabaseError) as error:
            print("something")
            print(error)
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    return render(request, 'room_form.html', {})

def class_list(request):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT Cl.classname, CL.year, CL.roomno
        FROM class CL;
        """

        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlStr)
        result = crsr.fetchall()
        print(result)
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
        return render(request, 'class_list.html', {'result': result})
        
def children_class(request):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr1 = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr1 = """
        select cl.classname, cl.year, cl.totalchildren
        from class cl;
        """

        crsr = connection.cursor()
        sqlStr = """
        select U.firstname, U.lastname, DATE_PART('YEAR', AGE(CURRENT_DATE, U.birthdate)) as age, U.birthdate, e.type
        from U, enrollment e
        where U.userid = e.userid;
        """

        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlStr)
        result = crsr.fetchall()
        crsr1.execute(sqlStr1)
        result1 = crsr.fetchall()
        print(result)
        print(result1)
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
        return render(request, 'children_class.html', {'result':result, 'result1':result1})

def pickup_schedule(request):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT U.firstname, U.lastname, ENROLLMENT.pickuphour
        FROM ENROLLMENT 
        FULL JOIN DRIVER ON ENROLLMENT.driverid = DRIVER.userid
        FULL JOIN CHILD ON CHILD.userid = ENROLLMENT.userid
        FULL JOIN U ON U.userid = CHILD.userid
        WHERE DRIVER.userid = %s;
        """
        crsr1 = connection.cursor()
        sqlStr1 = '''
        SELECT DD.day
FROM DRIVER_DAY DD
FULL JOIN DRIVER D ON D.userid = DD.userid
WHERE D.userid = %s;
        '''
        # execute the data fetch SQL command along with the SQL placeholder values
        crsr1.execute(sqlStr1, (request.session["userid"],))
        result1 = crsr1.fetchall()
        crsr.execute(sqlStr, (request.session["userid"],))
        result = crsr.fetchall()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
    return render(request, 'pickup_schedule.html', {'result':result, 'result1':result1})

def program(request):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT P.name, op.year, cl.classname, users.firstname, users.lastname, r.roomno, E.date, e.pickuphour, dri.phonenumber, p.programid
        FROM ENROLLMENT E
        FULL JOIN CHILD C ON C.userid = E.userid
        FULL JOIN U ON U.userid = C.userid
        FULL JOIN CLASS CL ON cl.programid = e.programid AND cl.year = e.year AND cl.classname = e.class 
        FULL JOIN OFFERED_PROGRAM OP ON OP.programid = cl.programid AND op.year = cl.year
        FULL JOIN PROGRAM P on P.programid = op.programid
        FULL JOIN CAREGIVER CA ON cl.cgid = ca.userid
        FULL JOIN STAFF S ON s.userid = ca.userid
        FULL JOIN U users ON users.userid = s.userid
        FULL JOIN ROOM R ON r.roomno = cl.roomno
        FULL JOIN DRIVER D ON D.Userid = e.driverid
        Full Join staff ds ON ds.userid = d.userid
        FULL JOIN U dri ON dri.userid = ds.userid
        WHERE E.userid = %s;
        """
        crsr1 = connection.cursor()
        sqlStr1 = '''
        SELECT Ex.name
        FROM ENROLLMENT E
        FULL JOIN EXTRACURRICULAR_TAKING et ON et.userid = e.userid AND et.programid = e.programid AND et.year = e.year AND et.class = e.class
        FULL JOIN EXTRACURRICULAR EX ON EX.extracurricularid = et.extracurricularid
        WHERE et.userid = %s;
        '''
        crsr2 = connection.cursor()
        sqlStr2 = '''
        SELECT a.name, ac.starthour, ac.endhour, ac.day FROM ENROLLMENT E
FULL JOIN CLASS CL ON cl.programid = e.programid AND cl.year = e.year AND cl.classname = e.class 
FULL JOIN OFFERED_PROGRAM OP ON OP.programid = cl.programid AND op.year = cl.year
FULL JOIN ACTIVITY_SCHEDULE Ac ON ac.programid=op.programid AND ac.year = op.year
FULL JOIN ACTIVITY A on ac.activityid=a.id
WHERE e.userid = %s;
        '''
        
        crsr3 = connection.cursor()
        sqlStr3 = '''
        SELECT M.name, MS.Hour, ms.day FROM ENROLLMENT E
FULL JOIN CLASS CL ON cl.programid = e.programid AND cl.year = e.year AND cl.classname = e.class 
FULL JOIN OFFERED_PROGRAM OP ON OP.programid = cl.programid AND op.year = cl.year
FULL JOIN MENU_SCHEDULE MS ON MS.programid = op.programid AND ms.year = op.year
FULL JOIN MENU M ON M.id = MS.menuid
WHERE e.userid = %s;;
        '''
        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlStr, (request.session["userid"],))
        result = crsr.fetchone()
        crsr1.execute(sqlStr1, (request.session["userid"],))
        result1 = crsr1.fetchall()
        crsr2.execute(sqlStr2, (request.session["userid"],))
        result2 = crsr2.fetchall()
        crsr3.execute(sqlStr3, (request.session["userid"],))
        result3 = crsr3.fetchall()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
    return render(request, 'program.html', {'result':result, 'result1':result1, 'result2': result2, 'result3': result3})

def manage_extracurricular(request, pid, year, cl):
    if request.method == 'POST':
        dropdown_value = request.POST.get('dropdown').split(',')
        print("Dropdown value:", dropdown_value)
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            # sql command to be executed for fetching the data
            sqlStr = """
        INSERT INTO EXTRACURRICULAR_TAKING VALUES (%s, %s, %s, %s, %s);
        """
        
        # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute(sqlStr, (request.session["userid"], pid, year, cl, dropdown_value[0]))
            connection.commit()
            crsr.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated For Insert.')
        
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

            # create a cursor
        crsr = connection.cursor()
            # sql command to be executed for fetching the data
        sqlStr = """
        SELECT E.name, E.Day, E.hour, e.extracurricularid, en.userid
FROM EXTRACURRICULAR E
FULL JOIN EXTRACURRICULAR_TAKING ET ON et.extracurricularid = e.extracurricularid
FULL JOIN ENROLLMENT EN ON EN.userid = et.userid AND EN.programid = et.programid AND EN.year = et.year AND EN.class = et.class 
WHERE EN.userid = %s;
        """
        crsr1 = connection.cursor()
        sqlStr1 = """
        SELECT E1.extracurricularid, E1.name, E1.day, E1.hour
FROM EXTRACURRICULAR E1
WHERE NOT EXISTS (
    SELECT 1
    FROM EXTRACURRICULAR_TAKING ET
    JOIN ENROLLMENT EN ON ET.userid = EN.userid AND ET.programid = EN.programid AND ET.year = EN.year AND ET.class = EN.class
    JOIN EXTRACURRICULAR E2 ON ET.extracurricularid = E2.extracurricularid
    WHERE EN.userid = %s
      AND (E1.day = E2.day AND E1.hour = E2.hour)
)
ORDER BY DAY, HOUR;
        """
        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlStr, (request.session["userid"],))
        result = crsr.fetchall()
        crsr1.execute(sqlStr1, (request.session["userid"],))
        result1 = crsr1.fetchall()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
    return render(request, 'manage_extracurricular.html', {'result':result, 'result1':result1, 'pid':pid, 'year':year, 'cl':cl})

def delete_extracurricular_user(request, Eid, Uid, pid, year, cl):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        sqlstr='''
        DELETE FROM extracurricular_taking
        WHERE userid = %s AND extracurricularid = %s AND programid=%s AND year=%s AND class=%s;
        '''
        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlstr, (Uid, Eid, pid, year, cl))
        connection.commit()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        messages.info(request, error.diag.message_primary)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
    return redirect('main:manage_extracurricular', pid=pid, year=year, cl=cl)

def child_dailyreport(request):
    connection = None
    try:
        params = config()
        print('Connecting to the postgreSQL database ...')
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        # sql command to be executed for fetching the data
        sqlStr = """
        SELECT ROW_NUMBER () OVER (ORDER BY programid) , class, date, activityreport, eatingreport, link
        FROM Daily_report
        WHERE userid = %s;
        """

        # execute the data fetch SQL command along with the SQL placeholder values
        crsr.execute(sqlStr, (request.session["userid"],))
        result = crsr.fetchall()
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
    return render(request, 'child_dailyreport.html', {'result': result})

def daily_reportform(request):
    if request.method=="POST":
        connection = None
        try:
            params = config()
            print('Connecting to the postgreSQL database ...')
            connection = psycopg2.connect(**params)

            # create a cursor
            crsr = connection.cursor()
            sqlStr = """
            INSERT into menu VALUES (%s, %s, %s, %s, %s);
            """
            
            # execute the data fetch SQL command along with the SQL placeholder values
            crsr.execute(sqlStr, (request.POST['firstname'], request.POST['lastname'], request.POST['date'], request.POST['activityreport'], request.POST['eatingreport'], request.POST['photolink']))
            connection.commit()
            crsr.close()
            return redirect('main:activity.html')
        except(Exception, psycopg2.DatabaseError) as error:
            print("something")
            print(error)
            messages.info(request, error.diag.message_primary)
        finally:
            if connection is not None:
                connection.close()
                print('Database connection terminated.')
    return render(request, 'daily_reportform.html', {})