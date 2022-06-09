// parsing each downstreamResults to upload the downstream link on Jenkins Dashboard
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
