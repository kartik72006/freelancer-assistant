from services.retrieval.embedding_service import EmbeddingService

service = EmbeddingService()

text1 = "React Developer"

text2 = "Frontend Engineer"

text3 = "Python Backend Developer"

embedding1 = service.generate_embedding(text1)
embedding2 = service.generate_embedding(text2)
embedding3 = service.generate_embedding(text3)

print(type(embedding1))
print(len(embedding1))
print(embedding1[:10])


print(type(embedding2))
print(len(embedding2))  
print(embedding2[:10])


print(type(embedding3))
print(len(embedding3))
print(embedding3[:10])