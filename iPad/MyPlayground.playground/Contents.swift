import UIKit

var greeting = "Hello, playground"

var imageViewWidth = screenSize.width
var x = Int.random(in: 1...12)

print(1,2,3,4,5, separator: "-")

print(greeting)

print(imageViewWidth)
print(screenSize.width)
print(x)
assert(1==1, "math failure")

for i in 1...10{
    debugPrint("Got number \(i).")
}

func printxtimes(num: Int8, letters: String){
    for _ in 1...num{
        debugPrint(letters)
    }
}


printxtimes(num: 8, letters: "hello")
