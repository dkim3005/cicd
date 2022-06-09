// parsing each downstreamResults to upload the downstream link on Jenkins Dashboard
// ex) url -> https://Xxxxx.xxxx.co.kr/ci/job/blahblah/job/qnx.upstream.downstream/163
// this regex logic is for extracting qnx.upstream.downstream.

// positive lookahead from /[0-9] ( /123 | /343 | /221 | .... | /1 )
// starts from / (slash)
// result : /(text_to_be_extracted)/123

if (downstreamResults) {
    Logger.info("Post pipeline downstream results:")
    downstreamResults.each { url, buildData ->
        Logger.info(url + " " + buildData.result)
        String resultIcon = ""
        if (buildData.result.equals("SUCCESS")) {
            resultIcon += "✔"
        } else if (buildData.result.equals("FAILURE")) {
            resultIcon += "❌"
        } else {
            resultIcon += '➖'
        }
        def pattern = (url =~ "([^\\/])+(?=\\/[0-9])")
        script.currentBuild.description += "<p>${resultIcon} ${buildData.result} : <a href=\"${url}\">${pattern[0][0]}</a></p>"
    }
}
