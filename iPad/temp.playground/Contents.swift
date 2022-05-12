import UIKit

func divby8(a:Int32) -> Int32 {
    return a/8
}

func add(a:Int, b:Int) -> Int{
    return a+b
}

var greeting = "Hello"
var anint:Int8 = 32

greeting.append(" world")
print(greeting)
print(anint)

var my8var:Int32 = 640
print(divby8(a: my8var))

print(add(a:12, b:42))

let screenSize: CGRect = UIScreen.main.bounds
print("Screen Width" + Int(screenSize.width).toString)
print(screenSize.height)

print(CGFloat.random(in: 4...18))


