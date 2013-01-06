
function showIt()
{
	var dbname = 'https://brucegne.cloudant.com/beg_demo/';
	var doc = '2d8297528c346dae14ad32b53a84dafe';
	
	alert( $.couch.db(dbname).openDoc(doc) );
}