from PycharmProjects.Reptile.ProxyPool.proxypool.api import app
from PycharmProjects.Reptile.ProxyPool.proxypool.schedule import Schedule

def main():

    s = Schedule()
    s.run()
    app.run()




if __name__ == '__main__':
    main()

