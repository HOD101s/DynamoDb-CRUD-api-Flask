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