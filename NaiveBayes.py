import csv
import random
import math
 
# -*- coding: utf-8 -*-

def wczytaj(nazwa):
	dane = list(csv.reader(open(nazwa, "rb")))
	for i in range(len(dane)):
		dane[i] = [float(x) for x in dane[i]]
	return dane
 
def podziel_dane(dane, wsp_pod):
	dane_nauki_ilosc = int(len(dane) * wsp_pod)
	dane_nauki = []
	dane_test = list(dane)
	while len(dane_nauki) < dane_nauki_ilosc:
		wiersz = random.randrange(len(dane_test))
		dane_nauki.append(dane_test.pop(wiersz))
	return [dane_nauki, dane_test]
 
def oddziel_chorych_zdrowych(dane):
	odzieleni = {}
	for i in range(len(dane)):
		pacjent = dane[i]
		if (pacjent[-1] not in odzieleni):
			odzieleni[pacjent[-1]] = []
		odzieleni[pacjent[-1]].append(pacjent)
	return odzieleni
 
def srednia(a):
	return sum(a)/float(len(a))
 
def odchylenie(a):
	sre = srednia(a)
	odchylenie = sum([pow(x-sre,2) for x in a])/float(len(a)-1)
	return math.sqrt(odchylenie)
 
def podsumowanie_jedno(dane):
	podsumowanie = [(srednia(wiersz), odchylenie(wiersz)) for wiersz in zip(*dane)]
	del podsumowanie[-1]# usun ostatni
	return podsumowanie
 
def podsumowanie_dla_klasy(dane):
	odzieleni = oddziel_chorych_zdrowych(dane)
	podsumowanie = {}
	for klucz, obiekt in odzieleni.iteritems():
		podsumowanie[klucz] = podsumowanie_jedno(obiekt)
	return podsumowanie
 
def policz_prawdo(x, srednia, odchylenie):
	e = math.exp(-(math.pow(x-srednia,2)/(2*math.pow(odchylenie,2))))
	return (1 / (math.sqrt(2*math.pi) * odchylenie)) * e
 
def policz_prawdo_dla_kazdego(podsumowanie, dane_test):
	prob = {}
	for klucz, pod in podsumowanie.iteritems():
		prob[klucz] = 1
		for i in range(len(pod)):
			sr, od = pod[i]
			x = dane_test[i]
			prob[klucz] *= policz_prawdo(x, sr, od)
	return prob
			
def przewiduj(podsumowanie, dane_test):
	prawdo = policz_prawdo_dla_kazdego(podsumowanie, dane_test)
	etykieta, pra = None, -1
	for klucz, p in prawdo.iteritems():
		if etykieta is None or p > pra:
			pra = p
			etykieta = klucz
	return etykieta
 
def przewidywanie(podsumowanie, dane_test):
	przewidywania = []
	for i in range(len(dane_test)):
		wynik = przewiduj(podsumowanie, dane_test[i])
		przewidywania.append(wynik)
	return przewidywania
 
def dokladnosc(dane_test, przewidywania):
	licznik = 0
	for i in range(len(dane_test)):
		if dane_test[i][-1] == przewidywania[i]:
			licznik += 1
	return (licznik/float(len(dane_test))) * 100.0
 
def main():
	
	dane = wczytaj('input.csv')
	dane_nauki, dane_test = podziel_dane(dane,0.67)
	print('\n\n')
	print('Ilosc pacjentow : {0} \n Pacjenci do nauki algorytmu : {1} \n Pacjenci do testowania : {2} \n').format(len(dane), len(dane_nauki), len(dane_test))
	podsumowanie = podsumowanie_dla_klasy(dane_nauki)
	prze = przewidywanie(podsumowanie, dane_test)
	dok = dokladnosc(dane_test, prze)
	print('Dokladnosc przewidzenia cukrzycy u pacjenta to : {0}%').format(dok)
 	print('\n\n')
main()

