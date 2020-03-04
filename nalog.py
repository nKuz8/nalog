import string
from datetime import timedelta, datetime, date


def getSum(percent, days, duty):
	return (float(percent.replace(',', '.'))*days*duty)/(360*100)


def getDaysCount(firstDate, lastDate):
	return (firstDate - lastDate).days - 1	


def makeDate(unformattedDateStr):
	""" Формирует дату из строки

		unformattedDateStr: строка с датой

		возвращает объект datetime
	"""
	return datetime(int(unformattedDateStr.split('.')[2]), 
			int(unformattedDateStr.split('.')[1]), int(unformattedDateStr.split('.')[0]))



def makeDateIntervalsFile(unsortedDatesFile, datesIntervalFile):
	""" Перерабатывает набор дат с процентами в интервалы дат с одинаковыми
	 	процентами

		
		unsortedDatesFile: файл с датами, скаченный с сайта
	 	ЦБ РФ в формате ДД.ММ.ГГГГ %
	 	datesIntervalFile: файл, в который будут записаны 
	 	интервалы дат 
	 	

	 	ничего не возвращает
	"""
	with open(unsortedDatesFile, 'r', encoding = 'UTF-8') as datesInput:
		with open(datesIntervalFile, 'w', encoding = 'UTF-8') as datesInterval:

			dateToCompare = datesInput.readline().split()[0]
			percentToCompare = datesInput.readline().split()[1]

			for line in datesInput:
				currentDate, currentPercent = line.split()[0], line.split()[1]

				if currentPercent != percentToCompare:
					lastDate = datetime(int(lastDate.split('.')[2]), int(lastDate.split('.')[1]), 
						int(lastDate.split('.')[0])).date()
					datesInterval.write(dateToCompare + ' ' + lastDate.strftime('%d.%m.%Y') + ' '  
						+ currentPercent + '\n')
					lastDate += timedelta(-1)
					dateToCompare, percentToCompare = lastDate.strftime('%d.%m.%Y'), currentPercent
				lastDate = currentDate		


def makeOutput(dateFirst, dateLast, duty, datesIntervalFile):
	""" Формирует набор дат с процентной ставкой и пошлиной

		dateFirst: дата начала
		dateLast: дата окончания
		duty: сумма для начисления пошлины
		datesIntervalFile: файл с интервалами дат

		возвращает массив для вывода
	"""	
	with open (datesIntervalFile, 'r', encoding = 'UTF-8') as datesIntervals:
		totalSumDuty = 0
		intervalsOutput = []

		for line in datesIntervals:
			firstDateToCheck = makeDate(line.split()[0])	
			lastDateToCheck = makeDate(line.split()[1])

			if dateLast <= firstDateToCheck and dateLast >= lastDateToCheck:
				percent = line.split()[2]

				if dateFirst <= firstDateToCheck and dateFirst >= lastDateToCheck: 
					daysCount = getDaysCount(dateLast, dateFirst) 
					intervalsOutput.append(str(daysCount) + ' дней ' + percent + '% ' + 
						str(round(getSum(percent, daysCount, duty), 2)) + ' руб')
					return intervalsOutput

				else: 
					daysCount = (dateLast - lastDateToCheck).days + 1
					totalSumDuty += getSum(percent, daysCount, duty)	
					intervalsOutput.append(str(daysCount) + ' дней ' + percent + '% ' 
						+ str(round(getSum(percent, daysCount, duty), 2)) + ' руб')

					for line in datesIntervals: #поиск интервала первой даты
						firstDateToCheck = makeDate(line.split()[0])	
						lastDateToCheck = makeDate(line.split()[1])
						percent = line.split()[2]

						if dateFirst <= firstDateToCheck and dateFirst >= lastDateToCheck: #интервал найден
							daysCount = getDaysCount(firstDateToCheck, dateFirst)
							totalSumDuty += getSum(percent, daysCount, duty)
							intervalsOutput.append(str(daysCount) + ' дней ' + percent + '% ' + 
								str(round(getSum(percent, daysCount, duty), 2)) + ' руб \nВсего: ' + 
								str(round(totalSumDuty, 2)) + ' руб')
							break

						else: #интервал не найден, выводим весь промежуток 
							daysCount = getDaysCount(firstDateToCheck, lastDateToCheck)
							totalSumDuty += getSum(percent, daysCount, duty)
							intervalsOutput.append(str(daysCount) + ' дней ' + percent + '% ' + 
								str(round(getSum(percent, daysCount, duty), 2)) + ' руб')

					return intervalsOutput


def main():
	makeDateIntervalsFile('data.txt', 'sorted_data.txt')

	duty = int(input('Введите пошлину: '))		
	firstDateIn = input('Введите первую дату: ')
	firstDate = datetime(int(firstDateIn.split('.')[0]), int(firstDateIn.split('.')[1]), 
		int(firstDateIn.split('.')[2]))
	lastDateIn = input('Введите вторую дату: ')
	lastDate = datetime(int(lastDateIn.split('.')[0]), int(lastDateIn.split('.')[1]), 
		int(lastDateIn.split('.')[2]))

	if firstDate > lastDate :
		firstDate, lastDate = lastDate, firstDate 

	outputList = makeOutput(firstDate, lastDate, duty, 'sorted_data.txt')
	
	for line in outputList:
		print(line)


if __name__ == "__main__":
    main()			

				



