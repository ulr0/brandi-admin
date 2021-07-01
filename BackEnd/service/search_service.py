from model.search_dao import SearchDao


class SearchService:
    def get_seller_name_search_list(self, connection, filters):

        filters["search_word"] = filters["search_word"] + "%"
        filters["limit"] = int(filters.get("limit", 10))

        if filters.get("limit") < 1:
            filters["limit"] = 1

        search_dao = SearchDao()
        sellers = search_dao.get_seller_name_search_list(connection, filters)

        return {"sellers": sellers}
