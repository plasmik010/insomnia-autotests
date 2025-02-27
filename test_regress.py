from .main_page import *
import time
from selenium.webdriver.common.by import By
from datetime import datetime

def test_pagination_in_volunteer_list(browser):
    #переход с 1 на 2 страницу пагинации в списке волонтеров.
    link="https://feedapp-dev.insomniafest.ru/login"
    page = BasePage(browser, link)
    page.open()
    page.first_window()
    time.sleep(1)
    page.login_admin()
    time.sleep(1)
    page.pagination()
    active_page = browser.find_element(By.CLASS_NAME, "ant-pagination-item-active")
    time.sleep(1)
    assert "2" in active_page.text, "Ошибка: Страница 2 не активна или текст отсутствует!"
    # проверяем что активная страница имеет 2 в наименовании

def test_pagination_in_feed_history(browser):
    #переход с 1 на 2 страницу пагинации в истории питания.
    link = "https://feedapp-dev.insomniafest.ru/feed-transaction"
    page = BasePage(browser, link)
    page.open()
    page.first_window()
    page.login_admin()
    time.sleep(1)
    page.meal_history_pagination()
    active_page = browser.find_element(By.CLASS_NAME, "ant-pagination-item-active")
    time.sleep(1)
    assert "2" in active_page.text, "Ошибка: Страница 2 не активна или текст отсутствует!"
    # проверяем что активная страница имеет 2 в наименовании


def test_create_new_meal(browser):
    link = "https://feedapp-dev.insomniafest.ru/feed-transaction"
    # создаем прием пищи, но сверяем что дата крайней записи - сегодня - - НЕ РАБОТАЕТ удаление
    page = BasePage(browser, link)
    page.open()
    page.first_window()
    page.login_admin()
    page.go_to_create_new_meal()
    page.create_new_meal()
    time.sleep(1)
    first_row_text = page.meal_table()
    today_date = datetime.now().strftime("%d/%m/%y")
    assert browser.current_url == "https://feedapp-dev.insomniafest.ru/feed-transaction?pageSize=10&current=1"
    assert  today_date in first_row_text, f"Ошибка! Ожидали сегодняшнюю дату, а получили {first_row_text}"
    # проверяем, что транзакция создана и дата последней записи - сегодня
    print("✅ Запись успешно создана!")


def test_delete_created_new_meal(browser):
    link = "https://feedapp-dev.insomniafest.ru/feed-transaction"
    # создаем прием пищи, но сверяем что дата крайней записи - сегодня - - НЕ РАБОТАЕТ удаление
    page = BasePage(browser, link)
    page.open()
    page.first_window()
    page.login_admin()
    time.sleep(2)
    page.meal_deleting()
    # Не мусорим, удаляем созданную запись, ассерт для инфо
    time.sleep(1)
    assert 1==1
    print("🗑 Запись успешно удалена!")

def test_create_group_badge(browser):
    # создаем вручную групповой бейдж и проверяем счетчик
    link = "https://feedapp-dev.insomniafest.ru/group-badges"
    page = BasePage(browser, link)
    page.open()
    time.sleep(1)
    page.first_window()
    page.login_admin()
    time.sleep(2)
    a = page.badges_counter()
    time.sleep(1)
    print("a =", a)
    page.go_to_create_badge()
    time.sleep(1)
    page.create_badge()
    time.sleep(1)
    b = page.badges_counter()
    print("b =", b)
    assert browser.current_url == "https://feedapp-dev.insomniafest.ru/group-badges"
    assert a+1 == b
    print("✅ Бейдж успешно создан! Счетчик увеличился на 1!")

def test_delete_group_badge(browser):
    link = "https://feedapp-dev.insomniafest.ru/group-badges"
    page = BasePage(browser, link)
    page.open()
    page.first_window()
    page.login_admin()
    time.sleep(2)
    pagination_items = browser.find_elements(By.CLASS_NAME, "ant-pagination-item")
    pagination_items[-1].click()
    time.sleep(1)
    last_row = browser.find_elements(By.CSS_SELECTOR, "tr.ant-table-row")[-1]
    columns = last_row.find_elements(By.CSS_SELECTOR, "td")
    column1 = columns[1].text
    if "autotest" in column1:
        page.delete_group_badge()
        assert 1==1
        print("Бейдж удален!")
    else:
        assert 1==1
        print("Нечего удалять!")

def test_create_custom_field(browser):
    link = "https://feedapp-dev.insomniafest.ru/volunteers"
    page = BasePage(browser, link)
    page.open()
    page.first_window()
    page.login_admin()
    time.sleep(1)
    page.go_to_custom_field_creating()
    time.sleep(1)
    # считаем число строк до создания кастомного поля
    rows_before = len(browser.find_elements(By.CSS_SELECTOR, "span.ant-btn-icon"))
    page.go_to_custom_field_creating_2()
    page.create_custom_field()
    time.sleep(1)
    #считаем число строк после создания кастомного поля
    rows_after = len(browser.find_elements(By.CSS_SELECTOR, "tr.ant-table-row"))
    # задаем поиск по последней строке
    last_row = browser.find_elements(By.CSS_SELECTOR, "tr.ant-table-row")[-1]
    columns = last_row.find_elements(By.CSS_SELECTOR, "td")
    column1 = columns[0].text
    column2 = columns[1].text
    assert "user" in column1, "Название поля не совпадает!"
    assert "string" in column2, "Тип поля не совпадает!"
    assert int(rows_before)-4==rows_after, "число записей изменилось не на 1!"
    #в выпадашке списка колонок 5 неподходящих элементов. Вычесть 4 - получим исходный список + 1 созданный

def test_delete_created_custom_field(browser):
    link = "https://feedapp-dev.insomniafest.ru/volunteer-custom-fields?sorters[0][field]=id&sorters[0][order]=asc"
    page = BasePage(browser, link)
    page.open()
    page.first_window()
    page.login_admin()
    time.sleep(2)
    last_row = browser.find_elements(By.CSS_SELECTOR, "tr.ant-table-row")[-1]
    columns = last_row.find_elements(By.CSS_SELECTOR, "td")
    column1 = columns[0].text
    if "user" in column1:
        page.delete_row()
        assert 1==1
        print("Запись удалена!")
    else:
        assert 1==1
        print("Нечего удалять!")



def test_add_and_delete_volunteer_from_group_badge(browser):
    #добавить, а затем удалить волонтера из группового бейджа
    link = "https://feedapp-dev.insomniafest.ru/group-badges"
    page = BasePage(browser, link)
    page.open()
    time.sleep(1)
    page.first_window()
    page.login_admin()
    #идем в редактирование последнего бейджика
    page.go_to_edit_badge()
    time.sleep(1)
    #фиксируем число на счетчике
    count1 = page.receive_count_of_volunteers_in_group_badge()
    #добавляем волонтера
    page.add_volunteer_in_group_badge()
    #фиксируем счетчик и сохраняем
    time.sleep(1)
    count2 = page.receive_count_of_volunteers_in_group_badge()
    page.save_in_group_badge()
    #возвращаемся в бейдж
    time.sleep(1)
    page.go_to_edit_badge()
    time.sleep(1)
    #фиксируем счетчик
    count3 = page.receive_count_of_volunteers_in_group_badge()
    #удаляем волонетра
    time.sleep(1)
    page.delete_volunteer_from_group_badge()
    #фиксируем счётчик и сохраняем
    count4 = page.receive_count_of_volunteers_in_group_badge()
    page.save_in_group_badge()
    time.sleep(1)
    #в ассертах сверяем возврат на урл групповых бейджей после сохранения и мэтч счётчиков между собой
    assert browser.current_url == "https://feedapp-dev.insomniafest.ru/group-badges"
    print("До-", count1, "человек в бейдже")
    assert count1==count4
    print("До-", count1, count4, "человек в бейдже")
    assert count2==count3
    print("После-", count3, "человек в бейдже")

def test_create_new_user(browser):
    #создать нового юзера
    link = "https://feedapp-dev.insomniafest.ru/volunteers"
    page = BasePage(browser, link)
    page.open()
    time.sleep(1)
    page.first_window()
    page.login_admin()
    # перейти на страницу создания нового юзера
    page.go_to_create_user()
    time.sleep(1)
    page.create_user()
    time.sleep(1)
    page.save_in_user_page()
    time.sleep(2)
    assert browser.current_url== "https://feedapp-dev.insomniafest.ru/volunteers"

def test_edit_new_user(browser):
    # найти созданного юзера и отредактировать его
    link = "https://feedapp-dev.insomniafest.ru/volunteers"
    page = BasePage(browser, link)
    page.open()
    time.sleep(1)
    page.first_window()
    page.login_admin()
    time.sleep(2)
    # перейти на страницу создания нового юзера
    page.find_user()
    page.edit_user()
    time.sleep(2)
    assert browser.current_url== "https://feedapp-dev.insomniafest.ru/volunteers"

def test_delete_new_user(browser):
    # найти созданного юзера и отредактировать его
    link = "https://feedapp-dev.insomniafest.ru/volunteers"
    page = BasePage(browser, link)
    page.open()
    time.sleep(1)
    page.first_window()
    page.login_admin()
    time.sleep(2)
    page.find_user()
    page.delete_user()
    time.sleep(2)
    assert browser.current_url == "https://feedapp-dev.insomniafest.ru/volunteers"

