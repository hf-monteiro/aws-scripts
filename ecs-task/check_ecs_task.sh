#!/bin/bash
set -x

CLUSTER=exp-dev-cluster # CLUSTER NAME HERE
FAMILY=exp-dev-app # ECS SERVICE NAME HERE

taskdef=$(aws ecs list-task-definitions --region us-east-1 --output text --query taskDefinitionArns[0])
for i in $taskdef; do
echo taskdef = $taskdef
if [ "$taskdef" == "None" ]; then
 echo "no task is running"
 exit 1
fi
done

defstatus=$(aws ecs describe-task-definition --region us-east-1 --task-definition $taskdef --output text --query taskDefinition.status)
echo $defstatus
sleep 3s ; echo check-1
if [ "$defstatus" == "ACTIVE" ]; then
task=$(aws ecs list-tasks --cluster $CLUSTER --desired-status RUNNING --region us-east-1 --output text --query taskArns[0])
  echo taskarn = $task

  fi
for i in $task; do

  if [ "$i" == "None" ]; then
     for n in {1..6};
      do

       echo "Taskarn is NONE so Retrying count , $n"
       echo "Sleep 30s...please wait"
       sleep 3;
       echo "Checking the task..."
       task=$(aws ecs list-tasks --cluster $CLUSTER --desired-status RUNNING --region us-east-1 --output text --query taskArns[0])
       if [ "$task" != "None" ];then
          echo "TASKARN IS STABLE"

          break

       else
          echo "Taskarn is NONE so Retrying count , $n"
          echo "Sleep 30s...please wait"
          sleep 3;
          task=$(aws ecs list-tasks --cluster $CLUSTER --desired-status RUNNING --region us-east-1 --output text --query taskArns[0])
          if [ "$n" == "6" ];then
            if [ "$task" == "None" ];then
             echo "UNSTABLE"
             exit 0
            fi
          else
            echo  " task $task"
             #$i = task

       fi
    fi
done
    fi

done

for i in $task; do
    taskdefarn=$(aws ecs describe-tasks --tasks $task  --cluster $CLUSTER --region us-east-1 --output text --query tasks[0].taskDefinitionArn)
    Status=$(aws ecs describe-tasks --tasks $i  --cluster $CLUSTER --region us-east-1 --output text --query tasks[0].lastStatus)
    echo taskstatus = $Status
    echo taskdef = $taskdef
    echo taskdefarn $taskdefarn


get_stable(){
echo "CHECKING THE STATUS OF TASK"
for i in {1..6};
do

  if [ "$Status" == "RUNNING" -a "$taskdef" == "$taskdefarn" ];then
     retval=1

     break

  else
     echo "Unstable ...Retrying count,$i"
     echo "Sleep 30s...please wait"
     sleep 3;
     retval=2
  fi

done

}

#call the function to check stable or not stable
get_stable
   if [ "$retval" ==  1 ]  ;then
       echo "STABLE"
   else
       echo "Unstable ....retry"
       get_stable
        if [ "$retval" !=  1 ]  ;then
            echo "UNSTABLE"
        else
            echo "STABLE"

        fi
   fi

done