# Apresentação Profissional — Art Similarity Vector Search

## Identidade e Proposta de Valor

O **Art Similarity Vector Search** é um sistema avançado de Recuperação de Imagens Baseada em Conteúdo (**Content-Based Image Retrieval - CBIR**) aplicado a acervos e galerias de belas artes. Ao superar os limites das buscas textuais tradicionais, o projeto possibilita a descoberta de obras por similaridade estética direta — comparando paletas cromáticas, traços estilísticos, composição espacial e pinceladas através de redes neurais convolucionais e busca vetorial de vizinhos mais próximos.

Diferenciais da solução:
- **Extração com Deep Learning**: Vetorização densa em 1.280 dimensões via **EfficientNetB0** pré-treinada na ImageNet com camada de Global Average Pooling.
- **Indexação Vetorial de Alta Performance**: Utilização do **Qdrant Vector Database** com indexação HNSW (*Hierarchical Navigable Small World*) e métrica de distância por Cosseno.
- **Arquitetura de Persistência Poliglota**: Separação rigorosa entre armazenamento de arquivos binários (**MinIO S3**), metadados relacionais (**MySQL 8**) e espaço vetorial latente (**Qdrant**).
- **Serviço de Consulta REST**: Endpoints assíncronos em **Flask** prontos para integração com clientes web e mobile modernos.

---

## Texto Estruturado para Publicação / Portfólio

> A catalogação tradicional de acervos culturais depende de descrições textuais que frequentemente falham em capturar nuances visuais ou estilos artísticos correlatos. Para resolver essa limitação, desenvolvi o **Art Similarity Vector Search**, um pipeline completo de recuperação visual (CBIR) que utiliza **EfficientNetB0** para transformar pinturas em embeddings de 1.280 dimensões e **Qdrant** para executar buscas por similaridade de cosseno em milissegundos. Adotando uma arquitetura de persistência poliglota — com MinIO para objetos e MySQL para dados relacionais —, o sistema demonstrou forte coerência semântica em testes reais, agrupando obras impressionistas de Monet com margem de cosseno de +0.2212 frente a estilos modernistas e abstratos. O projeto comprova proficiência em deep learning aplicado à visão computacional, bancos de dados vetoriais e arquitetura de sistemas orientada a dados.

---

## Resultados da Validação Real

- **Coleção Vetorial Criada**: Coleção `art_similarity` ativa no cluster Qdrant local na porta 6333, operando sob 1.280 dimensões e distância de cosseno.
- **Indexação de Acervo Visual**: Obras de diferentes períodos (Monet, Van Gogh, Picasso, Kandinsky) vetorizadas e indexadas com metadados estruturados.
- **Busca por Vizinhos Mais Próximos (k-NN)**: Validação de ordenação semântica — consulta com *Nenúfares no Lago* recuperou *Impressão, Nascer do Sol* com score `0.9946`, isolando com precisão estilos divergentes como Cubismo (`0.8348`) e Abstracionismo (`0.7734`).

---

## Evidências Visuais e Técnicas

1. **Diagrama Arquitetural de Busca Vetorial**: [`evidencias/arquitetura_busca_vetorial_art.png`](evidencias/arquitetura_busca_vetorial_art.png)
2. **Matriz de Similaridade de Cosseno entre Obras**: [`evidencias/matriz_similaridade_cosseno_obras.png`](evidencias/matriz_similaridade_cosseno_obras.png)
3. **Registro de Execução Real e Scores de Recuperação**: [`evidencias/log_execucao_real.txt`](evidencias/log_execucao_real.txt)
