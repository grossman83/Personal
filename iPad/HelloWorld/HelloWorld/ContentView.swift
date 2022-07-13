//
//  ContentView.swift
//  HelloWorld
//
//  Created by MARC GROSSMAN on 9/19/21.
//

import SwiftUI

let screenSize: CGRect = UIScreen.main.bounds

struct ContentView: View {
//    typealias Body = <#type#>
    
    
//    let x = Int.random(in: 1...5)
//    var imageViewWidth = screenSize.width
//    var imageViewHeight = screenSize.height

}
    var body: some View {
        VStack(spacing: 100.0) {
            Image("unicorn_clipArt").foregroundColor(/*@START_MENU_TOKEN@*/.blue/*@END_MENU_TOKEN@*/).frame(width: 3.0, height: 3.0).fixedSize().imageScale(.large)
            Image("unicorn_clipArt").foregroundColor(/*@START_MENU_TOKEN@*/.blue/*@END_MENU_TOKEN@*/).frame(width: 3.0, height: 3.0).fixedSize().offset(x: -200, y: 0.0)
            Image("unicorn_clipArt").foregroundColor(/*@START_MENU_TOKEN@*/.blue/*@END_MENU_TOKEN@*/).frame(width: 3.0, height: 3.0).fixedSize().offset(x: 200, y: 0.0)
            Button(action: {
                print("hello")
            }, label: {
                Text("Refresh Page")
            })
            .offset(x: /*@START_MENU_TOKEN@*/0.0/*@END_MENU_TOKEN@*/, y: /*@START_MENU_TOKEN@*/400.0/*@END_MENU_TOKEN@*/)
        }
    }
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        Group {
            ContentView()
//            ContentView()
//            ContentView()
        }
    }
}


//    print(imageViewWidth)
//    print(imageViewHeight)

    
//    @objc func updatePosition() {
//    func updatePosition() {
////        let maxX = View.imageViewWidth
////        let maxY = View.imageViewWidth
//        let xCoord = CGFloat.random(in: -200...200)
//        let yCoord = CGFloat.random(in: -400...600)
//        VStack(spacing: 100.0) {
//            Image("unicorn_clipArt").foregroundColor(/*@START_MENU_TOKEN@*/.blue/*@END_MENU_TOKEN@*/).frame(width: 3.0, height: 3.0).fixedSize()
//                .imageScale(.large)
//            Image("unicorn_clipArt").foregroundColor(/*@START_MENU_TOKEN@*/.blue/*@END_MENU_TOKEN@*/).frame(width: 3.0, height: 3.0).fixedSize().offset(x: xCoord, y: yCoord)
//            Image("unicorn_clipArt").foregroundColor(/*@START_MENU_TOKEN@*/.blue/*@END_MENU_TOKEN@*/).frame(width: 3.0, height: 3.0).fixedSize().offset(x: 200, y: 0.0)
//            Button(action: {
//                print("hello")
//                updatePosition()
//            }, label: {
//                Text("Refresh Page")
//            })
//            .offset(x: /*@START_MENU_TOKEN@*/0.0/*@END_MENU_TOKEN@*/, y: /*@START_MENU_TOKEN@*/400.0/*@END_MENU_TOKEN@*/)
//
//
//        UIView.animate(withDuration: 0.3) {
//            imageView.transform = CGAffineTransform(translationX: xCoord, y: yCoord)
//        }
//        }
//    }
