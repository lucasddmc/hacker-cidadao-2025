//
//  ContentView.swift
//  PrimeirosPassinhosApp
//
//  Created by Bruna Veiga Chalegre de Lira on 13/03/25.
//

import SwiftUI

struct ContentView: View {
    
    var body: some View {
        NavigationStack {
            ZStack (alignment: .top){
                ScrollView {
                    ZStack {
                        Image("background")
                            .resizable()
                            .scaledToFit()
                        
                        VStack {
                            VStack(spacing: 25) {
                                
                                Spacer()
                                
                                HStack(spacing: 35) {
                                    
                                    NavigationLink {
                                        consultasView()
                                    } label: {
                                        Image("consultas")
                                            .resizable()
                                            .scaledToFit()
                                            .frame(width: 80, height: 100)
                                    }
                                    
                                    NavigationLink {
                                        transporteView()
                                    } label: {
                                        Image("transporte")
                                            .resizable()
                                            .scaledToFit()
                                            .frame(width: 80, height: 100)
                                    }
                                    
                                    
                                    Button {
                                        
                                    } label: {
                                        Image("informacoes")
                                            .resizable()
                                            .scaledToFit()
                                            .frame(width: 80, height: 100)
                                    }
                                    
                                    
                                }
                                
                                HStack(spacing: 35) {
                                    Button {
                                        
                                    } label: {
                                        Image("beneficios")
                                            .resizable()
                                            .scaledToFit()
                                            .frame(width: 80, height: 100)
                                    }
                                    
                                    Button {
                                        
                                    } label: {
                                        Image("vacinas")
                                            .resizable()
                                            .scaledToFit()
                                            .frame(width: 80, height: 100)
                                    }
                                    
                                    Button {
                                        
                                    } label: {
                                        Image("leite")
                                            .resizable()
                                            .scaledToFit()
                                            .frame(width: 80, height: 100)
                                    }
                                }
                            }
                            .padding(.bottom, 94)
                            
                            Link(destination: URL(string: "https://t.me/lucasddmc_bot")!) {
                                Image("chatButton")
                                    .resizable()
                                    .scaledToFill()
                                    .frame(width: 176, height: 33)
                            }
                            
                        }
                        .padding(.bottom, 151)
                        
                    }
                }
                
                Image("bar")
                    .resizable()
                    .scaledToFill()
                    .frame(height: 135)
            }
            .ignoresSafeArea()
        }
        .navigationBarHidden(true)
        
    }
}

#Preview {
    ContentView()
}
