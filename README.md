# 🚀 Automação do Acesso à Arte com IA e Vetorização de Imagens

## Descrição

Este projeto visa a criação de um pipeline completo para a **coleta, processamento e organização** de dados de obras de arte, com foco em **busca visual** baseada em **inteligência artificial (IA)** e **vetorização de imagens**. Utilizando um **dataset público** com mais de **550 mil URLs** de obras, o objetivo principal é permitir buscas visuais eficientes e escaláveis.

**Nota:** O **front-end** deste projeto está em um repositório separado. Este repositório contém apenas o **back-end**, que fornece a API e realiza o processamento de dados. O front-end integra com esse back-end para permitir a busca visual.

## Funcionalidades

### 1. **Web Crawler com Selenium WebDriver**
   - O crawler percorre as páginas do dataset para identificar URLs com imagens válidas.
   - Inicialmente, o processo foi realizado com **20 mil imagens**, mas o sistema pode ser expandido para o conjunto completo, oferecendo resultados ainda mais robustos.

### 2. **Pipeline de Processamento**
   O pipeline é composto por **3 etapas principais** para cada obra de arte:
   - **📥 Download da Imagem:** O sistema baixa as imagens diretamente das URLs fornecidas.
   - **📝 Extração dos Metadados:** Informações como **título**, **autor** e **descrição** são extraídas para enriquecer a base de dados.
   - **🗂️ Armazenamento Distribuído:**
     - **MySQL** para armazenar os dados textuais.
     - **MinIO** para o armazenamento das imagens.
     - **Qdrant** para indexação e busca por vetores.

### 3. **Vetorização de Imagens**
   A vetorização das imagens foi realizada utilizando o modelo **EfficientNetB0**, gerando vetores de **1280 dimensões** que representam semanticamente os aspectos visuais das obras. Esses vetores foram então indexados no **Qdrant**, possibilitando buscas por **similaridade visual** de maneira rápida e eficiente.

### 4. **Integração com o Front-End**
   O **front-end** deste projeto não está incluído neste repositório, mas ele foi desenvolvido em **Angular 19+**. O front-end interage com o back-end (a API deste repositório) para realizar buscas visuais, proporcionando uma experiência fluida e intuitiva ao usuário.

## Tecnologias Utilizadas

- **Python** & **Selenium**: Para web scraping e extração de dados.
- **MySQL**: Banco de dados para armazenamento de metadados textuais.
- **MinIO**: Armazenamento distribuído para as imagens.
- **Qdrant**: Indexação e busca por similaridade visual.
- **TensorFlow** & **EfficientNetB0**: Para vetorização de imagens.
- **API**: O back-end é projetado para integração com o front-end desenvolvido em **Angular 19+**.

## Aplicações Futuras

O projeto foi finalizado por enquanto, mas há **grande potencial de expansão**:
- **Escalabilidade**: A base de dados pode ser ampliada, processando milhões de imagens com alto desempenho.
- **Busca Visual em App**: Imagine um aplicativo para museus, onde o usuário tira uma foto de uma obra e recebe informações sobre ela, incluindo obras visualmente semelhantes.
  
O código, os dados e o aprendizado estão disponíveis para futuras implementações e melhorias, com possibilidades reais de aplicação.

## Contribuições

Sinta-se à vontade para contribuir com melhorias, sugestões ou novos casos de uso. Caso tenha interesse em colaborar ou tenha dúvidas sobre o projeto, não hesite em entrar em contato!
