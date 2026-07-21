import time
from typing import Any, Dict, List, Optional

import numpy as np

from config.settings import CANDIDATE_K, MIN_SIMILARITY_SCORE, TOP_K


class SemanticRetriever:

    def search(
        self,
        query: str,
        query_embedding,
        vector_store,
        top_k: int = TOP_K,
        candidate_k: int = CANDIDATE_K,
        min_score: float = MIN_SIMILARITY_SCORE,
        where=None
    ) -> Dict[str, Any]:

        start_time = time.perf_counter()

        response = vector_store.search(
        query_embedding=query_embedding,
        top_k=candidate_k,
        where=where
    )
        results = []

        ids = response["ids"][0]
        documents = response["documents"][0]
        metadatas = response["metadatas"][0]
        distances = response["distances"][0]

        for id_, doc, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances
        ):

            similarity = 1 - distance

            results.append({
                "id": id_,
                "score": round(similarity, 4),
                "document": doc,
                "metadata": metadata
            })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        candidate_results = results[:candidate_k]

        filtered_results = [
            result
            for result in candidate_results
            if result["score"] >= min_score
        ]

        if not filtered_results:
            filtered_results=candidate_results[:1]

        unique_results = self.remove_duplicates(filtered_results)

        if unique_results:
            average_score = (
                sum(result["score"] for result in unique_results)
                / len(unique_results)
            )
        else:
            average_score = 0.0

        stats: Dict[str, Any] = {
            "total_documents": len(results),
            "candidate_results": len(candidate_results),
            "filtered_results": len(filtered_results),
            "unique_results": len(unique_results),
            "average_similarity": round(average_score, 4),
            "top_score": unique_results[0]["score"] if unique_results else 0.0,
            "lowest_score": unique_results[-1]["score"] if unique_results else 0.0,
            "latency_ms": round(
                (time.perf_counter() - start_time) * 1000,
                2
            )
        }

        return {
            "results": unique_results[:top_k],
            "stats": stats
        }

    def remove_duplicates(
        self,
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        unique: List[Dict[str, Any]] = []
        seen_documents = set()

        for result in results:

            document_id = result["id"]

            if document_id not in seen_documents:
                unique.append(result)
                seen_documents.add(document_id)

        return unique
    