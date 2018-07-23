var timeString = function(timestamp) {
    t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}

var newsTemplate = function(data) {
    var title = data["title"]
    var url = data["url"]
    var source = data["source"]
    var category =data["category"]
    var created_at =data["created_at"]

    // data-xx 是自定义标签属性的语法
    // 通过这样的方式可以给任意标签添加任意属性
    // 假设 d 是 这个 div 的引用
    // 这样的自定义属性通过  d.dataset.xx 来获取
    // 在这个例子里面, 是 d.dataset.id
    var n = `<li class="news-cell" style="margin-top: 10px;">
        <p>
            <a href="{{url}}" target="_blank" style="text-decoration: none;"> {{title}}</a>

            <em style="font-size: 12px; color: #666;">[{{source }} {{category} } {{created_at}}]</em>
        </p>
    </li>

    `
    return n

}


var insertNews = function(data) {
    var newsCell = newsTemplate(data)
    // 插入 news-list
    var newsList = e('.page')
    newsList.insertAdjacentHTML('beforeend', newsCell)
}


var loadNews = function() {
    // 调用 ajax api 来载入数据
    apiAll(function(r) {
        console.log('load all', r)
        // 解析为 数组
        var news = JSON.parse(r)

        // 循环添加到页面中
        for(var i = 0; i < news.length; i++) {
            var new = news[i]
            insertNews(new)
        }
    })
}




var __main = function() {
    loadNews()
}

__main()






