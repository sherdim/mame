# -*- coding: utf-8 -*-
# Симуляция динамики популяции вирусов

import numpy
import random
import pylab


class Virus(object):
    """
    Репрезентация простого вируса (без моделирования резистентности к лекарствам).
    """
    def __init__(self, pBirth, pClear):
        """
        Инициализирует экземпляр класса Virus, сохраняет все параметры как атрибуты экземпляра.
        
        pBirth: Максимальная рождаемость (число в диапазоне 0-1). 
        
        pClear: Вероятность исчезновения (число в диапазоне 0-1).
        """
        self.pBirth=pBirth
        self.pClear=pClear
        

    def getMaxBirthProb(self):
        """
        Возвращает вероятность максимальной рождаемости.
        """
        return self.pBirth

    def getClearProb(self):
        """
        Возвращает вероятность исчезновения.
        """
        return self.pClear

    def doesClear(self):
        """
        Определяет исчезает ли на этом временной шаге данная вирусная частица из организма пациента или нет.
        Возвращает True с вероятностью self.getClearProb, иначе - False.
        """
        return (random.random() <= self.getClearProb() )

    
    def reproduce(self, popDensity):
        """
        Стохастически репродуцирует данную вирусную частицу на данном временном шаге.
        Частица воспроизводит себе подобную с вероятностью
            self.pBirth * (1 - popDensity).
        
        Если воспроизведение происходит, то функция reproduce() создает и возвращает 
        новый экземпляр класса Virus со свойствами, идентичными родительскому экземпляру 
        (такие же значения pBirth и pClear).

        popDensity: плотность популяции (число с плавающей запятой), определяемая как отношение 
        текущей популяции вирусов к максимально возможной популяции.         
        
        Возвращает: 
        - новый экземпляр класса Virus, представляющего потомка данной частицы
        - вызывает исключение NoChildException, если данная частица не вопроизвелась.
        """
        if random.random() <= (self.pBirth * (1 - popDensity)):
            return Virus(self.pBirth, self.pClear)
        else:
            raise( NoChildException )


class Patient(object):
    """
    Репрезентация упрощенного пациента. Пациент не принимает лекарства и его популяции вирусов 
    не имеют резистнетности.
    """    

    def __init__(self, viruses, maxPop):
        """
        Функция инициализации, сохраняет параметры viruses и maxPop как атрибуты объекта.

        viruses: массив, представляющий популяцию вирусов (список (list) экземпляров класса Virus)

        maxPop: максимально возможная популяция вирусов для этого пациента (целое число)
        """

        self.viruses=viruses
        self.maxPop=maxPop
        

    def getViruses(self):
        """
        Возвращает популяцию вирусов данного пациента.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Возвращает максимальный объем популяции.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Дает общий размер текущей популяции вирусов. 
        Возвращает целое число.
        """
        return len(self.viruses)     


    def update(self):
        """
        Обновляет состояние вирусной популяции данного пациента за один временной шаг.
                      
        Возвращает целое число - размер популяции к концу обновления.
        """

        # Обновляем список вирусов, если еще есть живые частицы
        
        self.viruses=[v for v in self.viruses if not v.doesClear()]
        
        # Расчитывает плотность популяции
        
        popDensity=self.getTotalPop()/self.getMaxPop()
        
        # Проводим операцию вопроизведения каждого из вирусов
        
        vvNew=[]
        for v in self.viruses:
            try:
                vvNew.append(v.reproduce(popDensity))
            except NoChildException:
                pass
        
        # Добавляем новорожденных вирусят в популяцию данного пациента
        
        self.viruses.extend(vvNew)
        
        return len(self.viruses)



class ResistantVirus(Virus):
    """
    Репрезентация вируса, имеющего резистентность к лекарствам.
    """   

    def __init__(self, pBirth, pClear, resistances, pMutat):
        """
        Инициализирует экземпляр класса ResistantVirus, сохраняет все параметры как атрибуты экземпляра.
        
        pBirth: Максимальная рождаемость (число в диапазоне 0-1). 
        
        pClear: Вероятность исчезновения (число в диапазоне 0-1).

        resistances: Словарь (dictionary) с именами лекарств и указателем текущей 
        резистентности данной частицы к данному лекарству (True или False).
        e.g. {'sfeducin':False, 'abibanol':False} означает, что данный вирус не имеет
        резистентности ни к сфедуцину, ни к абибанолу.

        pMutat: Вероятность мутации для данной вирусной частицы (число в диапазоне 0-1).
        С этой вероятностью потомок приобретает или теряет резистентность к лекарству.
        """
        Virus.__init__(self, pBirth, pClear)
        self.resistances=resistances
        self.pMutat=pMutat
        
        self.pBirth=pBirth
        self.pClear=pClear


    def getResistances(self):
        """
        Возвращает резистинетность данного вируса.
        """
        return self.resistances

    def getMutProb(self):
        """
        Возвращает вероятность мутации для данного вируса.
        """
        return self.pMutat

    def isResistantTo(self, drug):
        """
        Проверяет резистинетность данной вирусной частицы к лекарству.
        
        drug: Лекарство (строка с названием)

        Возвращает True если этот экземпляр вируса резистентен к этому 
        лекарству, иначе - False.
        """
        return self.resistances.get(drug, False)


    def reproduce(self, popDensity, activeDrugs):
        """
        Стохастически репродуцирует данную вирусную частицу на данном временном шаге. 
        
        Частица воспроизводит себе подобную только если она резистентна ко 
        всем лекарствам в списке activeDrugs. Если хотя бы одно лекарство из 
        списка действует на данную частицу - она не воспроизведется.
        Если вирус резистентен ко всем лекарствам в списке, то тогда вирус 
        воспроизведется с вероятностью 
            self.pBirth * (1 - popDensity).                       

        
        Если воспроизведение происходит, то функция reproduce() создает и 
        возвращает новый экземпляр класса ResistantVirus со свойствами, 
        идентичными родительскому экземпляру 
        (такие же значения pBirth, pClear и pMutat).
        
        Резистентность потомка к каждому из лекарств наследуется от 
        родительского экземпляра с вероятностью 1-pMutat, и с вероятностью
        pMutat изменяется. Например, если вирусная частица резистентна к
        айдарцинину, но не резистентна к абибанолу, и self.pMutat равна 0.1, 
        то в 10% случаев ее потомок потеряет резистентность к айдарцинину, 
        но скорее всего в 90% случаев сохранит ее. И, наоборот, в 10% случаев 
        потомок приобретет резистентность к абибанолу, а в 90% будет неустойчив 
        к нему как и родительский экземпляр.
        

        popDensity: плотность популяции (число с плавающей запятой), 
        определяемая как отношение текущей популяции вирусов 
        к максимально возможной популяции.         
        
        activeDrugs: перечень названий лекарств, действующих в данный момент 
        на эту вирусную частицу (список строк).
        
        Возвращает новый экземпляр класса ResistantVirus, представляющего 
        потомка данной частицы.
        Вызывает исключение NoChildException, если данная частица 
        не вопроизвелась.
        """
        for d in activeDrugs:
            if not self.isResistantTo(d):
                raise( NoChildException )
            
        if random.random() <= (self.pBirth * (1 - popDensity)):
            
                mutresistances={k:(self.resistances[k] if (random.random()<(1-self.pMutat)) else
                        not self.resistances[k])
                    for k in self.resistances}
            
                return ResistantVirus(self.pBirth, self.pClear, 
                    mutresistances, self.pMutat)
        else:
            raise( NoChildException )
        
 

class TreatedPatient(Patient):
    """
    Репрезентация пациента. Пациент способен принимать лекарства, а 
    его популяция вирусов может приобретать резистнетность к этим лекарствам.
    """

    def __init__(self, viruses, maxPop):
        """
        Функция инициализации, сохраняет параметры viruses и maxPop как свойства объекта.
        Также инициализирует список лекарств, который изначально пустой.
        
        viruses: массив, представляющий популяцию вирусов

        maxPop: максимально возможная популяция вирусов для этого пациента
        """

        Patient.__init__(self, viruses, maxPop)
        self.drugs=[]


    def addPrescription(self, newDrug):
        """
        Назначает лекарство пациенту. 
        После добавления назначенного лекарства, оно действует на популяцию
        вирусов на всех последующих шагах. Если newDrug уже было прописано
        этому пациенту, то данный метод не имеет эффекта.

        newDrug: Название лекарства для введения пациенту (строка).

        Не возвращает ничего, лишь пополняет список активных лекарств.
        """

        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):
        """
        Возращает список лекарств, прописанных пациенту.
        """
        return self.drugs


    def getResistPop(self, drugResist):
        """
        Дает размер популяции вирусных частиц, устойчивых к данным лекарствам.

        drugResist: Список лекарств, резистентность к которым проверяется
        (список строк - например, ['sfeducin'] или ['sfeducin', 'abibanol'])

        Возвращает размер популяции вирус (целое число), резистентных ко всем
        лекарствам из списка drugResist.
        """

        N=0
        
        for v in self.viruses:
            if sum([not v.isResistantTo(d) for d in drugResist])==0:
                N+=1
                    
        return N


    def update(self):
        """
        Обновляет состояние вирусной популяции данного пациента за один временной шаг.
        
        Возвращает целое число - размер популяции к концу обновления.

        """

        self.viruses=[v for v in self.viruses if not v.doesClear()]
        
        popDensity=self.getTotalPop()/self.getMaxPop()
        vvNew=[]
        for v in self.viruses:
            try:
                vvNew.append(v.reproduce(popDensity, self.drugs))
            except NoChildException:
                pass
                
        self.viruses.extend(vvNew)
        
        return len(self.viruses)


class NoChildException(Exception):
    """
    NoChildException вызывается методом reproduce() в классах вирусов в случаях, 
    когда вирус не размножился. 
    Специальный класс для исключений можно использовать для вывода сообщений, статистики и пр.
    """

def simulationWithoutDrug(nVirus, maxPop, pBirth, pClear,
                          nTrials=30):
    """
    Симуляция без лекарств.
    Отображает на графике средний размер популяции вирусов на каждом 
    временном шаге.

    nVirus: начальный размер популяции (integer)
    maxPop: максимально возможная популяция вирусов (integer)
    pBirth: Максимальная рождаемость (float 0-1)        
    pClear: Вероятность исчезновения (float 0-1)
    nTrials: количество повторов симуляции для усреднения (integer)
    """
    
    nTime=300

    # массив нулей для временных шагов
    N=[0]*nTime
    
    for i in range(nTrials):
        
        vv=[Virus(pBirth, pClear) for i in range(nVirus)]
        patient = Patient(vv, maxPop)

        for time in range(len(N)):
            patient.update()
            N[time]+=(patient.getTotalPop())

    N=[n/float(nTrials) for n in N]
    
    time=range(len(N))
    pylab.plot(time, N, 's-')
    pylab.xlabel('time')
    pylab.ylabel('Population')
    pylab.legend(['avg'])
    pylab.title('Virus Population')
    
    pylab.show() 


def simulationWithDrug(nVirus, maxPop, pBirth, pClear, resistances,
                       pMutat, nTrials=30, t1=150):
    """
    Симуляция с действием лекарств.
    Отображает на графике средний размер популяции вирусов на каждом временном шаге.

    На каждой попытке на 150-м шаге добавляет sfeducin.
    Кроме графика средней вирусной популяции добавляет график количества
    вирусов, резистентных к этому лекарству.
    
    nVirus: начальный размер популяции (integer)
    maxPop: максимально возможная популяция вирусов (integer)
    pBirth: Максимальная рождаемость (float 0-1)        
    pClear: Вероятность исчезновения (float 0-1)
    resistances: Словарь с именами лекарств и указателем резистентности к ним
        (например, {'sfeducin': False})
    pMutat: Вероятность мутации для каждой вирусной частицы (float 0-1)
    nTrials: количество повторов симуляции для усреднения (integer)
    
    """

    nTime=t1 + 150
    N=[0]*nTime
    R=[0]*nTime
    
    for i in range(nTrials):
        
        vv=[ResistantVirus(pBirth, pClear, resistances, pMutat) for iVirus in range(nVirus)]
        patient = TreatedPatient(vv, maxPop)

        for time in range(len(N)):
            patient.update()
            N[time]+=(patient.getTotalPop())
            R[time]+=(patient.getResistPop(['sfeducin']))
            
            if time==t1:
                patient.addPrescription('sfeducin')

    N=[n/float(nTrials) for n in N]
    R=[n/float(nTrials) for n in R]
    
    xx=range(len(N))
    pylab.plot(xx, N, 's-')
    pylab.plot(xx, R, 'o-r')
    pylab.xlabel('time')
    pylab.ylabel('Population')
    pylab.legend(['total','resistant'])
    pylab.title('Virus Population')
    
    pylab.show() 


