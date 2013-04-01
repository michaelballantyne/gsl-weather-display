// Version 1.1 - 1/24/2013
// JavaScript Document
// This file is required for all USGS websites to employ.
// POCs: Tim Woods (twoods@usgs.gov); Ramona Neafie (rneafie@usgs.gov); Scott Horvath (shorvath@usgs.gov)
// DO NOT MODIFY any code beneath this unless approval provided by all POCs above.
// Updated on 1/24/13 to include switching between http and https based on protocol

function include(file)
{
  var script  = document.createElement('script');
  script.src  = file;
  script.type = 'text/javascript';
  script.defer = true;
 
  document.getElementsByTagName('head').item(0).appendChild(script);
}

if ("https:" == document.location.protocol) {
    /* secure */
	/* required JS files for Foresee, GSA Analystics, and USGS Analytics */
	// Version 1.0 - 1/4/2013
	include('https://my.usgs.gov/foresee/foresee-trigger.js');
	// Version 1.0 - 1/4/2013
	include('https://my.usgs.gov/scripts/analytics/federated-analytics.js');
	// Version 1.0 - 1/4/2013
	include('https://my.usgs.gov/scripts/analytics/googleanalytics.js');
	// Version 1.1 - 3/4/2013
	include('https://my.usgs.gov/scripts/analytics/usa-search.js');
} else {
    /* unsecure */
	/* required JS files for Foresee, GSA Analystics, and USGS Analytics */
	// Version 1.0 - 1/4/2013
	include('http://www.usgs.gov/foresee/foresee-trigger.js');
	// Version 1.0 - 1/4/2013
	include('http://www.usgs.gov/scripts/analytics/federated-analytics.js');
	// Version 1.0 - 1/4/2013
	include('http://www.usgs.gov/scripts/analytics/googleanalytics.js');
	// Version 1.1 - 3/4/2013
	include('http://www.usgs.gov/scripts/analytics/usa-search.js');
} 

// JavaScript Document