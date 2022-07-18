# Скрипт для замерения потребления памяти во время выполнения задачи
# Использую встроенную библиотеку cProfile
import cProfile
import meowpunk


cProfile.run('meowpunk.main()')
