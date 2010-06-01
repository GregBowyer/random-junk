(function() {
    var scripts = ['http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js', 
        'http://github.com/documentcloud/underscore/raw/4b2744a75adb3697ae2c99101704abdf512551dd/underscore-min.js'];

    function loadScript(url) {
        var script = document.createElement("script");
        script.type = 'text/javascript';
        script.charset = 'utf-8';
        script.src = url;
        document.documentElement.insertBefore(script, document.documentElement.firstChild);
        script.onreadystatechange = function () { if (script.readyState == 'complete' || script.readyState =='loaded') { loadScript(); }};
        script.onload = function () { loadScript(); }
        return true;
    };

    for each(var url in scripts) {
        loadScript(url);
    }
})();

(function() {
 console.log(
    _($('.product')).chain()
        .map(function(elem) { return $(elem).hasClass('csp-compact-offers') })
        .values()

);
 /*
document.getElementByTagName
var elems = document.getElementsByTagName('input')

for(var elemIndex in elems) {
    var elem = elems[elemIndex];
    if(elem.type == 'hidden' && elem.id.indexOf('deals') != -1 ) {
        console.log(elem);
    }
}
*/
})();
