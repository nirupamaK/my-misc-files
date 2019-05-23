### TASK 2 :
System spec - 
- 4 times Intel(R) Xeon(R) CPU E7-4830 v4 @ 2.00GHz
- 64GB of ram
- 2 tb HDD disk space
- 2 x 10Gbit/s nics
The server is used for SSL offloading and proxies around 25000 requests per second.
Please let us know which metrics are interesting to monitor in that specific case and how would you do that? What are the challenges of monitoring this?

### Here is my analysis for monitoring metrics for this case.

* Let's assumed that server is running `Apache` for SSL offloading and proxing purpose and the infrastructure is running on `Google Cloud Platform`.

* As server act as SSL offloading and proxy for typical HTTP application, is a CPU intensive task and would be good to monitor CPU and memory usage even though server has good enough hardware specs. However these are just basic checks to ensure the overall system health.

* Health checks and alerting policies for all necessary running services on the server.

* A logging agent is required like rsyslogd, logstash or google-fluentd (for GCP servers) can push the logs to monitoring systems such as ELK or Google Cloud's stackdriver. 

* As the server is question is a acting as SSL offloading for backend web application. Its important to keep track of following things:
  If SSL offloading server is apache using Logformat for example:
        
        ```
        Logformat “%t %h %{SSL_PROTOCOL}x %{SSL_CIPHER}x “%r” %b “%{Referer}i” “%{User-Agent}i”” ssl_combined
  	```

        - RemoteHostIP - %h
        - SSL_Protocols - %{SSL_PROTOCOL}x
        - user-agent - “%{User-Agent}i””

   However most of the time SSL logs are generally useful when some issue ocurred or for RCA later on.  

* For proactive monitoring from Application and Site Reliability point of view, as this server as proxy for a typical web application should be good monitor HTTP status code per request.

* The HTTP status codes can be filtered from HTTP access logs. Ideally the the number incoming requests for following status codes is important.

	- HTTP status 200 is for successful requests.
	- HTTP status 400/403/404 for bad request/forbidden/Not found.
        - HTTP status 500/502/503 for internal server errors/bad gateway/service unavailable.

* Monitoring number for incoming requests per second for each status code mentioned above in an individual chart (like a line graph simple and suitable) is important to track unusual spikes at specific point of time. An alerting policy should be configured for each error code, in case any number of error code goes beyond threshold limit.

* As server ideally dealt with 25K requests for second. If number incoming requests for 200 status, goes way beyond 25K/second, could be possibility for DOS/DDOS attack for public websites, should trigger alert and you may need to tune your mod_qos rate limit settings.

### To achieve this:

* In case infrastructure in on google cloud, GCP's stackdriver can be used to achieve this. The google-fluentd agent can be installed and configured to push http logs to GCP's stackdriver.

* Once you have structured logs pushed in stackdriver, log entires can be filtered based on fields. Here we are filtering HTTP status code field `(>%s)` from apache access logs, create a matrix for each HTTP status code. 
 
* These metrics are created as User-defined metrics in GCP Log-based metrics. The type of the metrics should be `counter`, shows the number of specific status code requests per second.

* Also using counter metrics alert policies could be created.

* Now on GCPs stackdriver an individual chart can be created using metrics, condition and desired threshold value. An alert policy can be configured in case threshold value is crossed once or 
  for certain time.

### Challenges of monitoring this scenario:

* Creating chart and configuring alerting policies means not always work done for SRE. There are always challenges.

* Proactive monitoring for any charts require manual human efforts, the alerting policies require continuous tuning and improvements, false alerts should be turned off and genuine should be correctly  configured.
  
* SREs needs to collect monitoring data for these charts, use knowledge and common sense and improve monitoring metrics accordingly, which is again a continuous human effort.     

* Not all HTTP status charts always provide with cause of issue or required RCA data, some RCAs require looking to actual logs records for respective timestamp.

* The public facing web sites are always prone to DOS/DDOS or all sorts for attacks, firewalls, WAF rules, rate limits require continuous improvements and tunings, which is again a manual SRE efforts by collecting past/present patterns from above charts.