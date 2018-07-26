var log = function() {
    console.log.apply(console, arguments)
}

var e = function(sel) {
    return document.querySelector(sel)
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
            <a href="${url}" target="_blank" style="text-decoration: none;"> ${title}</a>

            <em style="font-size: 12px; color: #666;">[${source } ${category} ${created_at}]</em>
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

var ajax = function(method, path,  data, reseponseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            reseponseCallback(r.response)
        }
    }
    // 发送请求
    r.send(data)
}

var loadNews = function() {
    // 调用 ajax api 来载入数据
    apiAll(function(res) {

        // 解析为 数组
        var news = JSON.parse(res)

        console.log('load all', news)

        // 循环添加到页面中
        for(var i = 0; i < news.length; i++) {
            var nw = news[i]
            insertNews(nw)
        }
    })
}

var apiAll = function(callback) {
    var path = '/api/v1/news'
    ajax('GET', path, '', callback)
}



var __main = function() {
    loadNews()
}

__main()






