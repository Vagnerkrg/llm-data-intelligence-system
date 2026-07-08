from src.application.intelligence_system import IntelligenceSystem



def test_count_products():

    system = IntelligenceSystem()


    response = system.ask(
        "Quantos produtos existem?"
    )


    assert (
        "32951"
        in response
    )



def test_category_with_more_products():

    system = IntelligenceSystem()


    response = system.ask(
        "Qual categoria possui mais produtos?"
    )


    assert (
        "cama_mesa_banho"
        in response
    )



def test_products_question():

    system = IntelligenceSystem()


    response = system.ask(
        "Quais produtos aparecem nos dados?"
    )


    assert (
        "Produto cadastrado"
        in response
    )