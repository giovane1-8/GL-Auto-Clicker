from Views.MainScreen import *
import ctypes

# ajusta o dpi para o click do mouse sair certo
#NÃO TIRAR
PROCESS_PER_MONITOR_DPI_AWARE = 2

ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

root = Tk()
MainScreen(root)
root.mainloop()

