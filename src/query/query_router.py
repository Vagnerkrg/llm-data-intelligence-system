from typing import Dict



class QueryRouter:
    """
    Routes user questions to the most appropriate dataset domain.

    Uses rule-based intent classification.
    """



    def __init__(self):

        self.routes = {

            "reviews": [

                "avalia",
                "avaliacao",
                "avaliação",
                "avaliacoes",
                "avaliações",
                "avaliar",
                "nota",
                "media",
                "média",
                "estrela",
                "estrelas",
                "comentario",
                "comentário",
                "satisfacao",
                "satisfação",
                "reclamacao",
                "reclamação",
                "opiniao",
                "opinião"

            ],



            "orders": [

                "pedido",
                "pedidos",
                "entrega",
                "entregas",
                "prazo",
                "atrasado",
                "status",
                "compra",
                "logistica",
                "logística"

            ],



            "products": [

                "produto",
                "produtos",
                "categoria",
                "categorias",
                "vendido",
                "venda",
                "mercadoria",
                "item",
                "itens",
                "catalogo",
                "catálogo"

            ],



            "customers": [

                "cliente",
                "clientes",
                "cidade",
                "estado",
                "localizacao",
                "localização"

            ]

        }



        self.priority = [

            "reviews",
            "orders",
            "products",
            "customers"

        ]



    def route(
        self,
        question: str
    ) -> Dict:

        question_lower = question.lower()


        scores = {}



        for domain, keywords in self.routes.items():

            score = 0


            for keyword in keywords:

                if keyword in question_lower:
                    score += 1


            scores[domain] = score



        for domain in self.priority:

            if scores[domain] > 0:

                return {

                    "domain": domain,

                    "confidence": scores[domain]

                }



        return {

            "domain": "general",

            "confidence": 0

        }