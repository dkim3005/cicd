node{
    
    def mailRecipients = 
    '''
    aaa@gmail.com
    '''
    
    String sshCommandReturn = sh (
        script: '''
        full=$(ssh xxxxxxxx@111.222.222.333 "df -h | grep somethingelse")
        echo ${full}
        '''
        ,returnStdout: true
        )

        // String sshCommandReturn =
        // 'somethingelse      2.5T  2.4T  100G  95% /DATA'

        def match= (sshCommandReturn =~ /[0-9]+(?=\%)/)
        int storageRatio = match[0]
        println "[INFO] data storage : ${storageRatio}%"
        //95 will be returned.
        
    if (storageRatio > 90){
        mail to: mailRecipients,
        subject: '[Jenkins] Jenkins Server Storage Alert',
        body: 
        'Warning ! Please free up current storage space !\n\n' +
        '- Current storage usage : ' + storageRatio + '%\n\n' +
        '- IP : xx.xxx.xxx.xxx\n\n' +
        '- Storage Mount Info (df -h) :\n   ' + sshCommandReturn
        println "[INFO] E-mail sent!"
    }else {
        println "[INFO] E-mail not sent."
    }
}
