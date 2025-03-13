//
//  consultasView.swift
//  PrimeirosPassinhosApp
//
//  Created by Bruna Veiga Chalegre de Lira on 13/03/25.
//

import SwiftUI

struct consultasView: View {
    
//    init() {
//            let appearance = UINavigationBarAppearance()
//            appearance.configureWithOpaqueBackground()
//            appearance.backgroundColor = UIColor.clear // Mantém a transparência ou a cor da barra
//            appearance.titleTextAttributes = [.foregroundColor: UIColor.white] // Cor do título
//            appearance.largeTitleTextAttributes = [.foregroundColor: UIColor.white]
//
//            // Define a cor do botão de voltar (Back Button)
//            UINavigationBar.appearance().tintColor = .white
//            
//            // Aplica a aparência configurada
//            UINavigationBar.appearance().standardAppearance = appearance
//            UINavigationBar.appearance().compactAppearance = appearance
//            UINavigationBar.appearance().scrollEdgeAppearance = appearance
//        }
    
    var body: some View {
        NavigationStack {
            ZStack(alignment: .top) {
                Image("backConsultas")
                    .resizable()
                    .scaledToFill()
                
                Image("bar")
                    .resizable()
                    .scaledToFill()
                    .frame(height: 135)
                
                HStack {
                    NavigationLink {
                        ContentView()
                    } label: {
                        Image(systemName: "chevron.left") // Ícone padrão do botão de voltar
                            .foregroundColor(.white) // Define a cor do botão como branco
                            .font(.system(size: 20, weight: .bold)) // Ajusta tamanho e peso
                            .padding()
                            .background(Color.black.opacity(0.5)) // Fundo sutil para contraste
                            .clipShape(Circle()) // Deixa o botão redondo
                            .padding(.leading, 16) // Afasta da borda
                            .padding(.top, 50) // Ajusta a posição para não ficar sobreposto
                    }
                    
                    Spacer()
                }
            }
            .ignoresSafeArea()
        }
        .navigationBarHidden(true)
    }
}

#Preview {
    consultasView()
}
