from flask import Flask,render_template,request,redirect,session,jsonify
from DBConnection import Db
import datetime

import pandas as pd
import matplotlib.pyplot as plt
app = Flask(__name__)
app.secret_key="789"

@app.route('/',methods=['get','post'])
def login():
    if request.method=='POST':
        Username=request.form['textfield']
        Password=request.form['textfield2']
        db=Db()
        qry=db.selectOne("SELECT * FROM login WHERE username='"+Username+"'and passwords='"+Password+"'")
        if qry is not None:
            session['head']=""

            session['lg'] = "lin"
            session['lid'] = qry['loginid']
            if qry['usertype'] =='admin':
                return redirect('/admin_home')
            if qry['usertype'] =='user':
                session['cnt'] = 0
                return redirect('/user_home')
            else :
                return "Invalid User"
        else:
            return "User not Found"
    else:
        return render_template ('index.html')

@app.route('/change_password',methods=['get','post'])
def change_password():
    if session['lg']=="lin":
        if request.method=='POST':
            currentpassword=request.form['textfield']
            newpassword=request.form['textfield']
            confirm= request.form['textfield']
            db=Db()
            qry=db.selectOne("select * from login where passwords='"+currentpassword+"' and usertype='admin'")
            if qry is not None:
                if newpassword==confirm:
                    db=Db()
                    db.update("update login set passwords='"+confirm+"' where usertype='admin'")
                    return '<script>alert("Password changed successfully");window.location="/admin_home"</script>'
                else :
                    return '<script>alert("Password dismatch");window.location="/admin_home"</script>'
            else:
                return '<script>alert("Incorrect Password");window.location="/admin_home"</script>'
        else:
            return render_template('admin/change password.html')
    else:
        return redirect('/')

@app.route('/add_chapter_manage',methods=['get','post'])
def add_chapter_manage() :
    if session['lg'] == "lin":
        if request.method=="POST":
            chapter=request.form['textfield']
            file=request.files['fileField']
            date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            file.save(r"C:\Users\USER\PycharmProjects\SiLingo\static\file\\"+date+'.pdf')
            p="/static/file//"+date+'.pdf'

            db = Db()
            res=db.selectOne("SELECT * FROM lesson WHERE chapter='"+chapter+"' AND pdf='"+str(p)+"'")
            if res is not None :
                return '<script>alert("Already existing");window.location="/add_chapter_manage"</script>'
            else:

                qry=db.insert("insert into lesson values('','"+chapter+"','"+str(p)+"')")
                # return '<script>alert("Added");window.location="/add_chapter_manage"</script>'
                return redirect('/add_chapter_manage')
        else:
            return render_template('admin/Lesson.html')
    else:
        return redirect('/')



@app.route('/view_lession')
def view_lession():
    if session['lg'] == "lin":
        db = Db()
        qry=db.select("SELECT * FROM lesson")
        return render_template('admin/Chapter Manage.html',data=qry)
    else:
        return redirect('/')

@app.route('/user_lesson')
def user_lesson():
    session['head']="Lesson"
    if session['lg'] == "lin":
        db = Db()
        qry=db.select("SELECT * FROM lesson")
        return render_template('user/user_lesson.html',data=qry)
    else:
        return redirect('/')

@app.route('/Complaint')
def Complaint():
    if session['lg'] == "lin":
        db = Db()
        qry = db.select("SELECT * FROM user,complaint WHERE user.userid = complaint.userid")
        return render_template('admin/Complaint.html',data=qry)
    else:
        return redirect('/')

@app.route('/lesson',methods=['get','post'])
def lesson():
    if session['lg'] == "lin":
        if request.method=='POST':
            chapter = request.form['textfield']
            file = request.files['fileField']
            db = Db()
            return render_template('admin/Lesson.html')
    else:
        return redirect('/')


@app.route('/reply/<cid>',methods=['get','post'])
def reply(cid):
    if session['lg'] == "lin":
        if request.method == 'POST':
            reply=request.form['textarea']
            db = Db()
            db.update("update complaint set reply='"+reply+"', replydate=curdate() where compid='"+cid+"'")
            return '<script>alert("Reply sent successfully");window.location="/Complaint"</script>'
        else:
            return render_template('admin/reply.html')
    else:
        return redirect('/')


@app.route('/suggestion')
def suggestion():
    if session['lg'] == "lin":
        db = Db()
        qry = db.select("SELECT * FROM user,suggestion WHERE user.userid = suggestion.userid")
        return render_template('admin/Suggestion.html')
    else:
        return redirect('/')


@app.route('/view_user')
def view_user():
    if session['lg'] == "lin":
        db = Db()
        qry=db.select("SELECT * FROM user,login WHERE user.userid= login.loginid")
        return render_template('admin/View User.html',data=qry)
    else:
        return redirect('/')


@app.route('/admin_home')
def adminhome():
    if session['lg'] == "lin":
        db = Db()
        return render_template('adminindex.html')
    else:
        return redirect('/')


@app.route('/user_home')
def userhome():
    if session['lg'] == "lin":
        db = Db()
        session['head']=""
        session['total']="5"
        session['r']=0
        return render_template('userindex.html')
    else:
        return redirect('/')



@app.route('/edit')
def edit():
    if session['lg'] == "lin":
        db = Db()
        return render_template('admin/admin home.html')
    else:
        return redirect('/')

@app.route('/view')
def view():
    if session['lg'] == "lin":
        db = Db()
        qry=db.select("SELECT * FROM lesson")
        return render_template('admin/admin home.html')
    else:
        return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    if session['lg'] == "lin":
        db = Db()
        qry=db.delete("DELETE FROM lesson WHERE  lid='"+id+"'")
        return '<script>alert("Deleted successfully");window.location="/view_lession#aa"</script>'
    else:
        return redirect('/')

@app.route('/logout')
def logout():
       session.clear()
       session['lg']=""
       return redirect('/')

######################################################userandroid########################


@app.route('/and_login',methods=['post'])
def and_login():
    db=Db()
    username=request.form['u']
    password=request.form['p']
    res=db.selectOne("SELECT * FROM login WHERE username='"+username+"' AND passwords='"+password+"'")
    print(res)
    if res is not None:
        print("iff")
        return jsonify(status="ok",lid=res['loginid'],type=res['usertype'])
    else:
        return jsonify(status="ok")


@app.route('/and_reg',methods=['post'])
def and_reg():
    db=Db()
    name=request.form['na']
    email=request.form['em']
    phone=request.form['phon']
    password=request.form['passwd']
    resn = db.selectOne("SELECT * FROM login WHERE  username='" +email+ "'")
    if resn is not None:
        return jsonify(status="no")
    else:
        res=db.insert("INSERT INTO login VALUES('','"+email+"','"+password+"','user')")
        res1=db.insert("INSERT INTO user VALUES('"+str(res)+"','"+name+"','"+email+"','"+phone+"' )")
        return jsonify(status="ok")

@app.route('/and_profile',methods=["post"])
def and_profile():
    db=Db()
    login=request.form['login']

    res=db.selectOne("Select * From user where userid='"+login+"'")
    return jsonify(status="ok",data=res)


@app.route('/and_lesson',methods=["post"])
def and_lesson():
    db=Db()
    # lid=request.form['lid']

    res=db.select("Select * From lesson")
    return jsonify(status="ok",data=res)

@app.route('/and_send_complaint',methods=["post"])
def and_send_complaint():
    db=Db()
    c=request.form['comp']
    cid = request.form['id']
    res=db.insert("INSERT INTO complaint VALUES('','"+cid+"','"+c+"',curdate(),'pending','pending')")
    return jsonify(status="ok",data=res)

@app.route('/and_view_complaint',methods=["post"])
def and_view_complaint():
    db=Db()
    lid=request.form['id']
    # comp=request.form['lid']
    res=db.select("SELECT * FROM complaint WHERE userid='"+lid+"'")
    return jsonify(status="ok",data=res)

@app.route('/and_send_suggestion',methods=["post"])
def and_send_suggestion():
    db=Db()
    suggestion=request.form['sugg']
    lid = request.form['id']
    # comp=request.form['lid']
    res=db.insert("INSERT INTO suggestion VALUES('','"+lid+"','"+suggestion+"',curdate())")
    return jsonify(status="ok",data=res)


@app.route('/and_change_password',methods=["post"])
def and_change_password():
    db=Db()
    current=request.form['curr']
    new=request.form['new1']
    confirm = request.form['conf']
    lid = request.form['id']
    # comp=request.form['lid']

    res=db.selectOne("SELECT * FROM login WHERE loginid='"+lid+"' and passwords='"+current+"'")
    if res is not None:
        if current==new:
            return jsonify(status="invalid")
        else:
            if new == confirm:
                db = Db()
                db.update("update login set passwords='" + confirm + "' where loginid='"+lid+"'")
                return jsonify(status="ok")
            else:
                return jsonify(status="invalid")

    else:
        return jsonify(status="invalid")




@app.route('/Application')
def Application():
    db=Db()
    try:
        import Application
        obj=Application()
    except Exception as e:
        return redirect('/user_home')


@app.route('/result')
def result():
    db=Db()
    q=db.selectOne("select mark from test where userid='"+str(session['lid'])+"' and status='Finished' order by testid desc")
    return render_template("user/result.html",data=q)
@app.route('/test')
def test():
    # if session['lin'] == "1":
        session['head'] = "Test on "+str(datetime.datetime.now().strftime("%Y-%m-%d"))

        output = ["A", "B", "C", "D", "E", "F", "G", "H", "I",
                  "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        finaloutput=[]

        if session['cnt'] == 0:
            import random,os
            random.shuffle(output)

            for i in output[0:5]:
                j=0
                for filename in os.listdir(r"C:\Users\USER\PycharmProjects\SiLingo\static\dataSet\trainingData\\"+i):
                    j=j+1
                    if j == 1:
                        finaloutput.append('/static/dataSet/trainingData/'+i+'/'+filename)
                    else:
                        pass
            session['output']=finaloutput
            session['op']=output[0:5]
        else:
            session['output']=session['output']
            session['op'] = session['op']

        return render_template("user/view_sample_question.html",c=session['op'][session['cnt']],data=session['output'][session['cnt']], ln=len(output[0:5]), cnt=int(session['cnt']))
    # return redirect('/')
@app.route('/finishexm/<crct_ans>',methods=['post'])
def finishexm(crct_ans):
    # if session['lin'] == "1":
    #     return redirect('/')
    db=Db()
    btn = request.form['button']
    qry2=db.selectOne("select * from test where userid='"+str(session['lid'])+"' and date=curdate() and status='pending'")
    print("ddd",qry2)
    print(btn,"============================================",session['cnt'])
    # from test import startcam
    # user_ans=startcam(str(session['lid']),crct_ans)
    user_ans=request.form['r'].upper()
    print(user_ans,"==============================================================",crct_ans)
    if qry2 is not None:
        ciid = session['lid']
        # print(btn,"eeeeeeeeeeeeeee")

        if str(btn)=="FINISH":
            # print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
            session['cnt']=0
            print("ussssss",user_ans)
            print("crrrrrrrr",crct_ans)
            if user_ans == crct_ans:
                session['r'] = session['r'] + 1
                qry = "update test set mark=mark+1,status='Finished' where userid='" + str(session['lid']) + "' and date=curdate()"
                res = db.update(qry)
                print("cccc",res)
                return '''<script>alert("succesfully attended");window.location="/result#aa"</script>'''
            else:
                qry = "update test set status='Finished' where userid='" + str(session['lid']) + "' and date=curdate()"
                res = db.update(qry)
                return '''<script>alert("succesfully attended");window.location="/result#aa"</script>'''

        else:


                if btn=="NEXT":
                    print("duuuuuuuuuuuu",user_ans)
                    print("dcccccccc",crct_ans)
                    session['cnt'] = session['cnt'] + 1
                    if user_ans == crct_ans:
                        session['r']=session['r']+1
                        print("llllllllllllll")

                        qry = "update test set mark=mark+1 where userid='"+str(ciid)+"' and date=curdate() and status='pending'"
                        res = db.update(qry)
                        return redirect('/test#aa')


                    else:
                        return redirect('/test#aa')
    else:
        print("oooooooooooooooooooooooooooo")
        print("uuuuuuuu",user_ans)
        print("ccccccc",crct_ans)
        if user_ans == crct_ans:
            session['cnt'] = session['cnt'] + 1
            session['r'] = session['r'] + 1
            qry = "insert into test values(null,'" + str(session['lid']) + "',curdate(),'1','pending')"
            res = db.insert(qry)
            print("aaaa",res)
            return redirect('/test#aa')


        else:
            session['cnt'] = session['cnt'] + 1
            qry = "insert into test values(null,'" + str(session['lid']) + "',curdate(),'0','pending')"
            res = db.insert(qry)
            print("bbb",res)
            return redirect('/test#aa')

@app.route('/progress')
def progress():
    # if session['lin'] == "1":
        session['head']="My Progress...."
        db=Db()
        q=db.select("select * from test where userid='"+str(session['lid'])+"' and status='Finished' order by date asc limit 3")
        if len(q)>0:
            m=datetime.datetime.now().strftime("%m")
            y =[]
            mylabels = ["Jan", "Feb", "March", "April","May","June","July","Aug","Sept","Oct","Nov","Dec"]
            newlabels=[]
            for i in range(0,int(m[1])):
                newlabels.append(mylabels[i])

                db=Db()
                i=i+1
                q=db.selectOne("select avg(mark) as m from test where userid='"+str(session['lid'])+"' and month(date)='"+str(i)+"' and status='Finished'")
                print(q)
                if q['m'] is not None:
                    y.append((q['m']))
                else:
                    y.append(0)


            data = {'year': newlabels,
                    'unemployment_rate': y
                    }

            df = pd.DataFrame(data)

            plt.plot(df['year'], df['unemployment_rate'], color='red', marker='o')
            # plt.title('', fontsize=14)
            plt.xlabel('Month', fontsize=10)
            plt.ylabel('Mark', fontsize=10)
            d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            plt.savefig(r"C:\Users\USER\PycharmProjects\SiLingo\static\graph\\" + d + '.jpg')
            p = '/static/graph/' + d + '.jpg'
            return render_template("user/progress.html",p=p)
        else:
            session['head']=""
            return render_template("user/progress.html")
    # return redirect('/')
if __name__ == '__main__':
    app.run(debug=True,port=4000,host="0.0.0.0")
