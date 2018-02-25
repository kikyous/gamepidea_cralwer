var is_chrome = /chrome|firefox/i.test( navigator.userAgent );

$.get("/index.json", function(data){
    var options = {
        source: data.data,
        fitToElement: true,
        theme: 'bootstrap4',
        items: 50,
        displayText: function(i){
            var en = i['en'];
            if(en)
                return i['cn'] + '(' + en + ')';
            else
                return i['cn']
        },
        afterSelect: function(i){
            location.href= '/' + i['cn'];
        }
    }
    if (is_chrome){
        options['updater'] = function(i){
            this.$menu.find('.active')[0].scrollIntoView(
                {block: "nearest", inline: "nearest"}
            );
            return i;
        }
    }
    $(".typeahead").typeahead(options).prop('placeholder', '搜索');
},'json');
