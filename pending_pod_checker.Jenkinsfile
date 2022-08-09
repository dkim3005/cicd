String mailRecipients = 'dongjin.kim@xxxxx.com'

properties([
    parameters([
        text(
            defaultValue: params.THRESHOLD_CONTAINER ?: '10',
            description: 'set threshold number',
            name: 'THRESHOLD_CONTAINER'
        ),
        text(
            defaultValue: params.THRESHOLD_TIME ?: '100',
            description: 'set threshold time',
            name: 'THRESHOLD_TIME'
        ),

        text(
            defaultValue: params.EMAIL_TO ?: mailRecipients,
            description: 'Send email reports to',
            name: 'EMAIL_TO'
        )
    ])
])

node {
    sshagent(['jenkins-docker']) {
        String numOfPendingContainer = sh(
                script: '''
                #!/bin/bash
                echo $(ssh xxxxxx@xx.xxx.xxx.xxx "kubectl get pods -n jenkins | grep Pending | awk -F ' ' {'print\\$5'} | awk -v time=\\$params.THRESHOLD_TIME -F 's' {'if(\\$1>time)print\\$1'} | wc -l")
                '''
                , returnStdout: true
        ).trim()

        println "[INFO] Threshold : number of container set to --> ${params.THRESHOLD_CONTAINER}"
        println "[INFO] Threshold : time(sec) set to --> ${params.THRESHOLD_TIME}"
        println "[INFO] Current Pending Container : ${numOfPendingContainer}"

        String report = "<h3>⚠[Kubernetes Warning] POD Scheduling Delay</h3> <p> ⌛ Number of unscheduled PODs :&nbsp;<strong> ${numOfPendingContainer} </strong> (over than ${params.THRESHOLD_TIME}sec) </p> <br><br><a href='${env.JOB_URL}'>Go to pending POD checker</a>"

        if (numOfPendingContainer.toInteger() > params.THRESHOLD_CONTAINER.toInteger()) {
            emailext body: report,
                    mimeType: 'text/html',
                    to: params.EMAIL_TO.replace('\n', ', '),
                    subject: '[CICD IVI] k8s POD Scheduling Delay'
        }
    }
}
