def write_ids():
    products = []
    product_ids = {}
    id = 0
    with open('transactions.csv', 'r') as transactions_f:
        with open('products.csv', 'w') as products_f:
            products_f.writelines('PROD_CODE;PROD_ID\n')
            for line in transactions_f:
                product_code = line.split(';')[0]
                if product_code != 'PROD_CODE':
                    if product_code not in products:
                        products.append(product_code)
                        product_ids[product_code] = id
                        products_f.write(f'{product_code};{id}\n')
                        id += 1
    return product_ids


def get_baskets(product_ids):
    baskets = {}
    with open('transactions.csv', 'r') as transactions_file:
        for line in transactions_file:
            line = line.replace('\n', '')
            product_code = line.split(';')[0]
            basket_id = line.split(';')[1]
            if product_code != 'PROD_CODE':
                if basket_id in list(baskets.keys()):
                    baskets[basket_id].append(product_ids[product_code])
                else:
                    baskets[basket_id] = [product_ids[product_code]]
    return baskets


def get_doubletons_in_basket(basket):
    doubletons = []
    doubleton = []
    basket.sort()
    for i in range(len(basket)):
        for j in range(i + 1, len(basket)):
            doubleton.append(basket[i])
            doubleton.append(basket[j])
            doubletons.append(doubleton)
            doubleton = []
    return doubletons


def get_doubletons(baskets):
    all_doubletons = []
    for basket in list(baskets.values()):
        doubletons_in_basket = get_doubletons_in_basket(basket)
        for doubleton in doubletons_in_basket:
            all_doubletons.append(doubleton)
    return all_doubletons


def hash_func(doubleton, products_count, multiplicator):
    return (multiplicator * doubleton[0] + doubleton[1]) % products_count


def main():
    product_ids = write_ids()
    baskets = get_baskets(product_ids)
    products_count = len(list(product_ids.keys()))
    all_doubletons = get_doubletons(baskets)
    singleton_count = [0] * products_count

    deleted_count = 0

    for doubleton in all_doubletons:
        for el in doubleton:
            singleton_count[el] = singleton_count[el] +  1

    for doubleton in all_doubletons[:]:
        first_el = doubleton[0]
        second_el = doubleton[1]

        if singleton_count[first_el] < 3 or singleton_count[second_el] < 3:
            all_doubletons.remove(doubleton)
            deleted_count += 1

    print(f"Deleted singletons: {deleted_count}")

    bitmaps = {}
    number_of_hash_functions = 10
    doubletons_count = {}

    for i in range(number_of_hash_functions):
        multiplicator = i * products_count // 100
        hash_values_count = [0] * products_count
        for doubleton in all_doubletons:
            hash_value = hash_func(doubleton, products_count, multiplicator)
            hash_values_count[hash_value] += 1

            if i == number_of_hash_functions - 1:
                if str(doubleton) in list(doubletons_count.keys()):
                    doubletons_count[str(doubleton)] += 1
                else:
                    doubletons_count[str(doubleton)] = 1
        bitmaps[multiplicator] = hash_values_count

    deleted_count = 0

    for doubleton in all_doubletons[:]:
        for i in range(number_of_hash_functions):
            multiplicator = list(bitmaps.keys())[i]
            hash_value = hash_func(doubleton, products_count, multiplicator)
            bitmap = bitmaps[multiplicator]

            if bitmap[hash_value] < 3:
                all_doubletons.remove(doubleton)
                deleted_count += 1
                break
            elif doubletons_count[str(doubleton)] < 3:
                all_doubletons.remove(doubleton)
                deleted_count += 1
                break

    print(f"Deleted doubletons: {deleted_count}")

    frequent_itemsets = []

    for i in range(len(singleton_count)):
        singleton_products = []
        if singleton_count[i] > 2:
            singleton_products.append(list(product_ids.keys())[i])
            frequent_itemsets.append(singleton_products)

    for doubleton in all_doubletons:
        doubleton_products = []
        for id in doubleton:
            product_code = list(product_ids.keys())[id]
            doubleton_products.append(product_code)
        frequent_itemsets.append(doubleton_products)

    print(frequent_itemsets)








if __name__ == '__main__':
    main()



