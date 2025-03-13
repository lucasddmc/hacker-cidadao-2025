//
//  transporteView.swift
//  PrimeirosPassinhosApp
//
//  Created by Bruna Veiga Chalegre de Lira on 13/03/25.
//

import SwiftUI

struct transporteView: View {
    var body: some View {
        NavigationStack {
            ZStack (alignment: .top){
                Image("backTransporte")
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
                
                Button {
                    
                } label: {
                    Image("downloadButton")
                        .resizable()
                        .scaledToFill()
                        .frame(width: 176, height: 33)
                        .padding(.top, 653)
                }
            }
            .ignoresSafeArea()
        }
        .navigationBarHidden(true)
    }
}

#Preview {
    transporteView()
}
