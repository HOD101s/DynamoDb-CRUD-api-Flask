import boto3
import uuid
import time
import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

ddb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
dbtable = ddb.Table("tasks")

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        try:
            dbtable.put_item(
                Item={
                    'id': uuid.uuid4().hex,
                    'added_date': int(time.time()),
                    'task': request.form["task"],
                }
            )
        except:
            return "Failed to Add Task"
        return redirect('/')
    else:
        tasks, taskCount = getTasks()
        if tasks == -1:
            return "Failed to Get Tasks"
        return render_template("index.html", tasks=tasks, taskCount=taskCount)

@app.template_filter('UNIX2Datetime')
def UNIX2Datetime(unix):
    return datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/delete/<string:id>/<int:added_date>')
def delete(id, added_date):
    try:
        dbtable.delete_item(
            Key={
                'id': id,
                'added_date': added_date
            }
        )
    except:
        return "Failed to Remove Task"

    return redirect('/')

@app.route('/update/<string:id>/<int:added_date>', methods=['POST','GET'])
def update(id, added_date):
    if request.method == 'POST':
        try:
            dbtable.update_item(
                Key={
                    'id': id,
                    'added_date': added_date
                },
                UpdateExpression='SET task = :val1',
                ExpressionAttributeValues={
                    ':val1': request.form["task"]
                }
            )
        except:
            return "Failed to Update Task"
        return redirect('/')
    else:
        response = dbtable.get_item(
            Key={
                'id': id,
                'added_date': added_date
            }
        )
        return render_template('update.html', task=response["Item"])

def getTasks():
    try:
        response = dbtable.scan()
        tasks = response["Items"]
        taskCount = response["Count"]
    except:
        return -1,-1
    return tasks, taskCount

if __name__ == '__main__':
    app.run(debug=True)