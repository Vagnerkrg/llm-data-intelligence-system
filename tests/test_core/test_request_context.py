from src.core.request_context import (
    create_request_id,
    set_request_id,
    get_request_id,
    clear_request_id
)



class TestRequestContext:


    def test_create_request_id(self):

        request_id = create_request_id()


        assert isinstance(
            request_id,
            str
        )


        assert len(
            request_id
        ) > 0



    def test_set_and_get_request_id(self):

        request_id = set_request_id(
            "test-request-123"
        )


        assert request_id == (
            "test-request-123"
        )


        assert get_request_id() == (
            "test-request-123"
        )



    def test_clear_request_id(self):

        set_request_id(
            "temporary-id"
        )


        clear_request_id()


        new_id = get_request_id()


        assert isinstance(
            new_id,
            str
        )


        assert new_id != (
            "temporary-id"
        )