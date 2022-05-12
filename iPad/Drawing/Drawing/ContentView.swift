//
//  ContentView.swift
//  Drawing
//
//  Created by MARC GROSSMAN on 9/18/21.
//

import SwiftUI

struct ContentView: View {
    
    var body: some View {
//        Text("Hello, world!")
//            .padding()
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
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
