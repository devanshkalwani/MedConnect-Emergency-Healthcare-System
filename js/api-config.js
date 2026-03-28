(function () {
    const storedBase = localStorage.getItem("medconnect_api_base");
    const candidates = [
        storedBase,
        "http://127.0.0.1:8001/api",
        "http://127.0.0.1:8000/api",
    ].filter(Boolean);
    // #region agent log
    fetch('http://127.0.0.1:7335/ingest/9d10bee9-2430-4471-b0be-893509ed00ae',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'1dca52'},body:JSON.stringify({sessionId:'1dca52',runId:'run-2',hypothesisId:'H6',location:'js/api-config.js:8',message:'api-config loaded',data:{storedBase:!!storedBase,candidateCount:candidates.length},timestamp:Date.now()})}).catch(()=>{});
    // #endregion

    async function medconnectFetch(path, options = {}) {
        const normalizedPath = path.startsWith("/") ? path : `/${path}`;
        let lastNetworkError = null;
        let lastResponse = null;
        // #region agent log
        fetch('http://127.0.0.1:7335/ingest/9d10bee9-2430-4471-b0be-893509ed00ae',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'1dca52'},body:JSON.stringify({sessionId:'1dca52',runId:'run-1',hypothesisId:'H1',location:'js/api-config.js:13',message:'medconnectFetch start',data:{path:normalizedPath,candidateCount:candidates.length,method:options.method||'GET'},timestamp:Date.now()})}).catch(()=>{});
        // #endregion

        for (const base of candidates) {
            try {
                const response = await fetch(`${base}${normalizedPath}`, options);
                lastResponse = response;
                // #region agent log
                fetch('http://127.0.0.1:7335/ingest/9d10bee9-2430-4471-b0be-893509ed00ae',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'1dca52'},body:JSON.stringify({sessionId:'1dca52',runId:'run-1',hypothesisId:'H2',location:'js/api-config.js:19',message:'candidate response received',data:{base,status:response.status,ok:response.ok,path:normalizedPath},timestamp:Date.now()})}).catch(()=>{});
                // #endregion

                if (response.status < 500) {
                    localStorage.setItem("medconnect_api_base", base);
                    return response;
                }
            } catch (err) {
                lastNetworkError = err;
                // #region agent log
                fetch('http://127.0.0.1:7335/ingest/9d10bee9-2430-4471-b0be-893509ed00ae',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'1dca52'},body:JSON.stringify({sessionId:'1dca52',runId:'run-1',hypothesisId:'H1',location:'js/api-config.js:28',message:'candidate network error',data:{base,path:normalizedPath,errorName:err?.name||'unknown'},timestamp:Date.now()})}).catch(()=>{});
                // #endregion
            }
        }

        if (lastResponse) {
            return lastResponse;
        }

        // #region agent log
        fetch('http://127.0.0.1:7335/ingest/9d10bee9-2430-4471-b0be-893509ed00ae',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'1dca52'},body:JSON.stringify({sessionId:'1dca52',runId:'run-1',hypothesisId:'H1',location:'js/api-config.js:40',message:'all candidates failed',data:{path:normalizedPath,hasLastNetworkError:!!lastNetworkError},timestamp:Date.now()})}).catch(()=>{});
        // #endregion
        throw lastNetworkError || new Error("Unable to connect to backend API");
    }

    window.MEDCONNECT_API_BASE = localStorage.getItem("medconnect_api_base") || candidates[0];
    window.medconnectFetch = medconnectFetch;
})();
