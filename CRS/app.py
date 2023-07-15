from flask import Flask,render_template,send_from_directory,url_for,request,session,redirect,json
from flask_mysqldb import MySQL
import MySQLdb.cursors
app = Flask(__name__)

app.secret_key = 'd3baaacbc62b49cea72e2cfab4cbea0162669bd96e47d1081e4e49eafc199e18'

## database credentials
app.config['MYSQL_HOST'] = '192.168.40.30'
app.config['MYSQL_USER'] = 'sdr'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'only_for_pralay'

mysql = MySQL(app)  
## Db connection end here

##displaying login page
@app.route('/')
def index():
    return render_template('login.html',title="Criminal Record System | Login",error='',emerr='',passerr='')

@app.route('/checklogin/', methods=['GET', 'POST'])
def checkcredential():
    err = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        if request.form['email'] == '' and request.form['password'] == '':
            err = 'All Fields Are Required'
            return render_template('login.html',title="Criminal Record System | Login",error=err)
        elif request.form['email'] == '':
            err = 'Email Is Required'
            return render_template('login.html',title="Criminal Record System | Login",error ='',emerr=err)
        elif request.form['password'] == '':
            err = 'Password Is Required'        
            return render_template('login.html',title="Criminal Record System | Login",error='',passerr=err)
        else:
            userid  = request.form['email']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cusers WHERE username = % s AND password = % s', (userid, password, ))
            user = cursor.fetchone()
            if user and user['status'] != 1:
                session['loggedin'] = True
                session['name'] = user['name']
                session['userid'] = user['username']
                return render_template('dashboard.html')
            else:
                err = "You are not authorised to logged in..."
                return render_template('login.html', error=err)
    return render_template('login.html', error='')        


## logout module
## function for logout users                      
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('name', None)
    return redirect(url_for('index')) 

## module for dashboard page
## function for dashboard
@app.route('/dashboard/')
def home():
    if session.get('loggedin') is None:
        return redirect(url_for('index'))
    else:
        return render_template('dashboard.html')
    
##
# module for managing police staff 
@app.route('/policestation/')
def police():
    if session.get('loggedin') is None:
        return redirect(url_for('index'))
    else:
        return render_template('policestaff.html')
    
## function for adding police station information
@app.route('/addpsInfo', methods=['POST'])
def addpsInfo():
    if session.get('loggedin') is None:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            psname = request.form['psname']
            pscode = request.form['pscode']
            psaddress = request.form['psadd']
            psphone = request.form['psphone']
            print(psname,pscode,psaddress,psphone)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO `police_station`(`ps_name`,`ps_code`,`ps_address`, `ps_phone`) VALUES (%s,%s,%s,%s)', (psname, pscode, psaddress, psphone))
            mysql.connection.commit()
            return json.dumps({'code': '1', 'status': 'Record Saved Successfully'})
        
## function for open crime page
@app.route('/policestaff/') 
def openCrime():
    if session.get('loggedin') is None:
        return redirect(url_for('index'))
    else:
        return render_template('police.html')
    
    
@app.route('/addStaff', methods=['POST'])
def addStaff():
    if session.get("loggdin") is None:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            stname = request.form['name']
            staddress = request.form['address']
            strank = request.form['rank']
            sid = request.form['p_id']
            sps = request.form['psName']
            stphone = request.form['phone']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO `police_staff`(`name`, `address`, `designation`, `st_phone`) VALUES (%s,%s,%s)', (stname, staddress, strank, stphone))
            mysql.connection.commit()
            return json.dumps({'code': '1', 'status': 'Record Saved Successfully'})
        
@app.route('/fetchData', methods=['POST'])
def fetchData():
    if session.get("loggedin") is None:
        return redirect(url_for('index'))           
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM police_station')
        data = cursor.fetchall()
        return json.dumps({'code': '1', 'result': data})
    
    
@app.route('/fetchrecordbyid', methods=['POST'])
def fetchrecordbyid():
    if session.get("loggedin") is None:
        return redirect(url_for('index'))
    else:
        _id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM police_station WHERE id= %s',_id)
        _data = cursor.fetchone()
        print(_data)
        return json.dumps({'code': '1', 'result': _data})
            
    
@app.route('/updatepsinfo', methods=['POST'])
def updatepsinfo():
    if session.get("loggedin") is None:
        return redirect(url_for('index'))
    else:
        _ps_name = request.form['p_name']
        _ps_code = request.form['p_code']
        _ps_address = request.form['p_add']
        _ps_phone = request.form['p_ph']
        _ps_id = request.form['p_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        _sqlQue = "UPDATE `police_station` SET ps_name= %s, ps_code= %s, ps_address= %s, ps_phone=%s WHERE id=%s";
        _data = (_ps_name,_ps_code,_ps_address,_ps_phone,_ps_id)
        cursor.execute(_sqlQue,_data)
        mysql.connection.commit()
        return json.dumps({'code': '1', 'status': 'Record Updated Successfully'})
        
@app.route('/deletebyid',methods=['POST'])
def deletebyid():
    if session.get("loggedin") is None:
        return redirect(url_for('index'))
    else:
        _id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        _sqlDel = "DELETE FROM `police_station` WHERE id=%s";
        _data = (_id)
        cursor.execute(_sqlDel,_data)
        mysql.connection.commit()
        return json.dumps({'code': '1', 'status': 'Record Deleted Successfully'})
                

@app.route('/showCategory')
def showCategory():
    if session.get('loggedin') is None:
        return redirect(url_for('index'))
    else:
        return render_template('crimecategory.html')
    
@app.route('/criminalpersons')
def criminalPersons():
    if session.get('loggedin') is None:
        return redirect(url_for('index'))
    else:
        return render_template('criminal.html')
        
@app.route('/report')
def report():
    if session.get('loggedin') is None:
        return redirect(url_for('index'))
    else:
        return render_template('report.html')

@app.route('/search')
def search():
    if session.get('loggedin') is None:
        return redirect(url_for('index'))
    else:
        return render_template('search.html')
                

if __name__ =='__main__':
    app.run(debug=True,port=8081)