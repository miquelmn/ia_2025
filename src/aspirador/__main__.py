from aspirador import joc, joc_gui, agent


#agents = [agent.AspiradorTaula()]
#agents = [agent.AspiradorReflex()]
agents = [agent.AspiradorMemoria()]

#hab = joc.Aspirador(agents)
hab = joc_gui.Aspirador(agents)
hab.comencar()
