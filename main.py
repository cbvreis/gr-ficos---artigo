import gzip as gz
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


def extract():
    f = gz.open('tempo-on-espanha_vs_chile-2014.txt.gz')
    f_content = f.readlines()
    values_on = []
    for line in f_content:
        l = line.rstrip()
        values_on.append(float(l.decode())/60)
    f = gz.open('tempo-off-espanha_vs_chile-2014.txt.gz')
    f_content = f.readlines()
    values_off = []
    for line in f_content:
        l = line.rstrip()
        values_off.append(float(l.decode())/60)
    return values_on, values_off


def extract_txt():
    f = open('log.txt')
    f_content = f.readlines()
    values_on = []
    values_off = []
    cont=0
    for line in f_content:
        try:
            line = line.split("|")
            on_time = line[1].split(":")[1]
            off_time = line[3].split(":")[1]
            values_on.append(int(on_time)/60)
            values_off.append(int(off_time)/60)
        except:
            print("Ops")
    return values_on, values_off


def cdf(values):
    total = float(len(values));
    cnt = 0;
    values.sort()
    last = values[0];
    a = []
    b = []
    for data in values:
        if data != last:
            a.append(last);
            b.append(cnt / total)
            cnt += 1;
            last = data;
        else:
            cnt += 1;

    a.append(last)
    b.append(cnt / total)
    return a, b


def chart(x, y, w_x, w_y, title):
    avg_x = np.average(x)
    avg_y = np.average(y)

    avg_wx = np.average(w_x)
    avg_wy = np.average(w_y)

    plt.plot(x, y, color="gray", label = "Valores Reais")
    plt.plot(w_x, w_y, color="black", label = "Valores Gerador")

    #Avg tempo de ON x tempo de OFF
    plt.plot(avg_x, avg_y, 'b.', label='Avg Real', marker="x", color="gray")
    plt.plot(avg_wx, avg_wy, 'b.', label='Avg Gerador', marker="x", color="black")

    #títulos e legendas
    plt.title(title + "- Valores Reais x Valores Gerador")
    plt.xlabel(title + " t(min)")
    plt.ylabel("P " + title + " <= 1")
    plt.legend()
    plt.show()


def chart_hist(values):
    recounted = Counter(values)
    print(recounted)
    plt.title("Histograma de valores tempo de On")
    plt.hist(values, bins=20)
    plt.show()


if __name__ == '__main__':
    on, off = extract()
   # chart_hist(on)
    workload_on, workload_off = extract_txt()

    values_on, perc_on = cdf(on)
    values_off, perc_off = cdf(off)

    work_values_on, work_values_on_perc = cdf(workload_on)
    work_values_off, work_values_off_perc = cdf(workload_off)

    # chart ontime
    chart(values_on, perc_on, work_values_on, work_values_on_perc, "Tempo de ON")

    # chart offtime
    chart(values_off, perc_off, work_values_off, work_values_off_perc, "Tempo de OFF")
