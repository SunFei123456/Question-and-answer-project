
// 1.点击按钮,发送请求,进行判断,
const sentRequest = () => {
    // 获取发送验证码按钮元素
    let sendEmail = document.getElementById("captcha-btn")
    // 点击按钮,发送请求,进行判断,
    sendEmail.addEventListener("click", (event) => {
            countdown()
            //  阻止默认冒泡事件
            event.preventDefault()
            // 获取邮箱的里面的值
            let emailValue = document.getElementById("exampleInputEmail1").value
            // 调取后端提供的接口
            const xhr = new XMLHttpRequest()
            console.log(emailValue)
            let url = "/sunfei/captcha/email?email=" + emailValue
            xhr.open('GET', url)
            xhr.send()
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4)
                    if (xhr.status >= 200 && xhr.status < 300) {
                        let response = xhr.response
                        let responseObj = JSON.parse(response)
                        console.log(responseObj)
                        if (responseObj.code === 200) {
                            // countdown()
                            console.log("请求成功")
                        } else {
                            alert("发送失败,请重试")
                        }
                    } else {
                        console.log(Error("请求失败"))
                    }

            }
        }
    )
}

// 2. 点击完毕之后,进入按钮元素的禁用状态,60s秒之后进行解除禁用,并在原本发送验证码的按钮上进行读秒
const countdown = () => {
    let countdown = 5
    let btn = document.getElementById("captcha-btn")
    btn.disabled = true
    let timer = setInterval(function () {
        countdown--
        if (countdown > 0) {
            btn.innerHTML = countdown + "秒后重新发送"
        } else {
            btn.innerHTML = "重新发送"
            btn.disabled = false
            clearInterval(timer)
        }
    }, 1000)
}

// 整个html文件加载完毕之后再进行js代码文件的执行
window.onload = function () {
    sentRequest()
}

