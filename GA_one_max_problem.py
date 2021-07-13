{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "GA_one_max_problem.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyOLstBDjpMoXaIFLldeC1bo",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/yuuki-kusumoto/EC21/blob/main/GA_one_max_problem.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "bthOGrhtKqdy",
        "outputId": "2c6b7996-77db-42b3-ac7b-4bf46cfa8c17"
      },
      "source": [
        "pip install deap"
      ],
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Collecting deap\n",
            "\u001b[?25l  Downloading https://files.pythonhosted.org/packages/99/d1/803c7a387d8a7e6866160b1541307f88d534da4291572fb32f69d2548afb/deap-1.3.1-cp37-cp37m-manylinux2010_x86_64.whl (157kB)\n",
            "\r\u001b[K     |██                              | 10kB 13.9MB/s eta 0:00:01\r\u001b[K     |████▏                           | 20kB 19.7MB/s eta 0:00:01\r\u001b[K     |██████▏                         | 30kB 10.8MB/s eta 0:00:01\r\u001b[K     |████████▎                       | 40kB 8.7MB/s eta 0:00:01\r\u001b[K     |██████████▍                     | 51kB 5.5MB/s eta 0:00:01\r\u001b[K     |████████████▍                   | 61kB 6.4MB/s eta 0:00:01\r\u001b[K     |██████████████▌                 | 71kB 6.0MB/s eta 0:00:01\r\u001b[K     |████████████████▋               | 81kB 6.3MB/s eta 0:00:01\r\u001b[K     |██████████████████▋             | 92kB 6.2MB/s eta 0:00:01\r\u001b[K     |████████████████████▊           | 102kB 6.7MB/s eta 0:00:01\r\u001b[K     |██████████████████████▉         | 112kB 6.7MB/s eta 0:00:01\r\u001b[K     |████████████████████████▉       | 122kB 6.7MB/s eta 0:00:01\r\u001b[K     |███████████████████████████     | 133kB 6.7MB/s eta 0:00:01\r\u001b[K     |█████████████████████████████   | 143kB 6.7MB/s eta 0:00:01\r\u001b[K     |███████████████████████████████ | 153kB 6.7MB/s eta 0:00:01\r\u001b[K     |████████████████████████████████| 163kB 6.7MB/s \n",
            "\u001b[?25hRequirement already satisfied: numpy in /usr/local/lib/python3.7/dist-packages (from deap) (1.19.5)\n",
            "Installing collected packages: deap\n",
            "Successfully installed deap-1.3.1\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "LP7U8mvsIGyz",
        "outputId": "113dd4ed-50d0-49df-be26-3c7427322cbe"
      },
      "source": [
        "import random\n",
        "\n",
        "from deap import base\n",
        "from deap import creator\n",
        "from deap import tools\n",
        "\n",
        "creator.create(\"FitnessMax\", base.Fitness, weights=(1.0,))\n",
        "creator.create(\"Individual\", list, fitness=creator.FitnessMax)\n",
        "\n",
        "toolbox = base.Toolbox()\n",
        "toolbox.register(\"attr_bool\", random.randint, 0, 1)\n",
        "toolbox.register(\"individual\", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)\n",
        "toolbox.register(\"population\", tools.initRepeat, list, toolbox.individual)\n",
        "\n",
        "def evalOneMax(individual):\n",
        "    return sum(individual),\n",
        "\n",
        "toolbox.register(\"evaluate\", evalOneMax)\n",
        "toolbox.register(\"mate\", tools.cxTwoPoint)\n",
        "toolbox.register(\"mutate\", tools.mutFlipBit, indpb=0.05)\n",
        "toolbox.register(\"select\", tools.selTournament, tournsize=3)\n",
        "\n",
        "def main():\n",
        "    random.seed(64)\n",
        "\n",
        "#長さが100で0と1で表現される個体を300個作成\n",
        "    pop = toolbox.population(n=300)\n",
        "\n",
        "#交叉をする確率、突然変異をする確率を設定\n",
        "    CXPB, MUTPB = 0.5, 0.1\n",
        "\n",
        "    print(\"Start of evolution\")\n",
        "\n",
        "\n",
        "    fitnesses = list(map(toolbox.evaluate, pop))\n",
        "    for ind, fit in zip(pop, fitnesses):\n",
        "        ind.fitness.values = fit\n",
        "\n",
        "    print(\"  Evaluated %i individuals\" % len(pop))\n",
        "\n",
        "#個々の適応度を取得\n",
        "    fits = [ind.fitness.values[0] for ind in pop]\n",
        "\n",
        "    g = 0\n",
        "    mean = 0\n",
        "\n",
        "    while max(fits) < 100 and g < 1000:\n",
        "        g = g + 1\n",
        "        print(\"-- Generation %i --\" % g)\n",
        "\n",
        "#選択を行う\n",
        "        offspring = toolbox.select(pop, len(pop))\n",
        "        offspring = list(map(toolbox.clone, offspring))\n",
        "\n",
        "#交叉を行う\n",
        "        for child1, child2 in zip(offspring[::2], offspring[1::2]):\n",
        "\n",
        "            if random.random() < CXPB:\n",
        "                toolbox.mate(child1, child2)\n",
        "\n",
        "                del child1.fitness.values\n",
        "                del child2.fitness.values\n",
        "\n",
        "#DEAP公式ドキュメントの突然変異の条件を変更\n",
        "        for mutant in offspring:\n",
        "\n",
        "            if random.random() < MUTPB and sum(mutant) >= 95:\n",
        "                toolbox.mutate(mutant)\n",
        "                del mutant.fitness.values\n",
        "\n",
        "        for mutant in offspring:\n",
        "\n",
        "          if random.random() < MUTPB*2 and 80 <= sum(mutant) < 95:\n",
        "            toolbox.mutate(mutant)\n",
        "            del mutant.fitness.values\n",
        "\n",
        "        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]\n",
        "        fitnesses = map(toolbox.evaluate, invalid_ind)\n",
        "        for ind, fit in zip(invalid_ind, fitnesses):\n",
        "            ind.fitness.values = fit\n",
        "\n",
        "        print(\"  Evaluated %i individuals\" % len(invalid_ind))\n",
        "\n",
        "        pop[:] = offspring\n",
        "\n",
        "        fits = [ind.fitness.values[0] for ind in pop]\n",
        "\n",
        "        length = len(pop)\n",
        "        mean = sum(fits) / length\n",
        "        sum2 = sum(x*x for x in fits)\n",
        "        std = abs(sum2 / length - mean**2)**0.5\n",
        "\n",
        "        print(\"  Min %s\" % min(fits))\n",
        "        print(\"  Max %s\" % max(fits))\n",
        "        print(\"  Avg %s\" % mean)\n",
        "        print(\"  Std %s\" % std)\n",
        "\n",
        "    print(\"-- End of (successful) evolution --\")\n",
        "\n",
        "    best_ind = tools.selBest(pop, 1)[0]\n",
        "    print(\"Best individual is %s, %s\" % (best_ind, best_ind.fitness.values))\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    main()"
      ],
      "execution_count": 41,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "/usr/local/lib/python3.7/dist-packages/deap/creator.py:141: RuntimeWarning: A class named 'FitnessMax' has already been created and it will be overwritten. Consider deleting previous creation of that class or rename it.\n",
            "  RuntimeWarning)\n",
            "/usr/local/lib/python3.7/dist-packages/deap/creator.py:141: RuntimeWarning: A class named 'Individual' has already been created and it will be overwritten. Consider deleting previous creation of that class or rename it.\n",
            "  RuntimeWarning)\n"
          ],
          "name": "stderr"
        },
        {
          "output_type": "stream",
          "text": [
            "Start of evolution\n",
            "  Evaluated 300 individuals\n",
            "-- Generation 1 --\n",
            "  Evaluated 154 individuals\n",
            "  Min 44.0\n",
            "  Max 65.0\n",
            "  Avg 54.86333333333334\n",
            "  Std 4.300153744021451\n",
            "-- Generation 2 --\n",
            "  Evaluated 142 individuals\n",
            "  Min 48.0\n",
            "  Max 69.0\n",
            "  Avg 58.516666666666666\n",
            "  Std 3.499007795869517\n",
            "-- Generation 3 --\n",
            "  Evaluated 150 individuals\n",
            "  Min 52.0\n",
            "  Max 73.0\n",
            "  Avg 61.46333333333333\n",
            "  Std 3.178362611296748\n",
            "-- Generation 4 --\n",
            "  Evaluated 148 individuals\n",
            "  Min 56.0\n",
            "  Max 73.0\n",
            "  Avg 64.33\n",
            "  Std 3.205375693009017\n",
            "-- Generation 5 --\n",
            "  Evaluated 158 individuals\n",
            "  Min 60.0\n",
            "  Max 77.0\n",
            "  Avg 67.07666666666667\n",
            "  Std 3.039318271513407\n",
            "-- Generation 6 --\n",
            "  Evaluated 156 individuals\n",
            "  Min 61.0\n",
            "  Max 77.0\n",
            "  Avg 69.72\n",
            "  Std 2.758308660514098\n",
            "-- Generation 7 --\n",
            "  Evaluated 148 individuals\n",
            "  Min 65.0\n",
            "  Max 79.0\n",
            "  Avg 72.11666666666666\n",
            "  Std 2.1454732707626882\n",
            "-- Generation 8 --\n",
            "  Evaluated 160 individuals\n",
            "  Min 66.0\n",
            "  Max 80.0\n",
            "  Avg 73.90333333333334\n",
            "  Std 2.2673013817212273\n",
            "-- Generation 9 --\n",
            "  Evaluated 156 individuals\n",
            "  Min 70.0\n",
            "  Max 82.0\n",
            "  Avg 75.93\n",
            "  Std 1.9642895238054798\n",
            "-- Generation 10 --\n",
            "  Evaluated 148 individuals\n",
            "  Min 72.0\n",
            "  Max 82.0\n",
            "  Avg 77.54333333333334\n",
            "  Std 1.4147280853773163\n",
            "-- Generation 11 --\n",
            "  Evaluated 159 individuals\n",
            "  Min 72.0\n",
            "  Max 82.0\n",
            "  Avg 78.51333333333334\n",
            "  Std 1.4479257193959971\n",
            "-- Generation 12 --\n",
            "  Evaluated 169 individuals\n",
            "  Min 75.0\n",
            "  Max 85.0\n",
            "  Avg 79.45666666666666\n",
            "  Std 1.53235838569919\n",
            "-- Generation 13 --\n",
            "  Evaluated 172 individuals\n",
            "  Min 72.0\n",
            "  Max 84.0\n",
            "  Avg 80.09\n",
            "  Std 1.8802216181432054\n",
            "-- Generation 14 --\n",
            "  Evaluated 175 individuals\n",
            "  Min 74.0\n",
            "  Max 85.0\n",
            "  Avg 80.92333333333333\n",
            "  Std 1.8984525862454482\n",
            "-- Generation 15 --\n",
            "  Evaluated 188 individuals\n",
            "  Min 74.0\n",
            "  Max 88.0\n",
            "  Avg 81.73333333333333\n",
            "  Std 2.0612833111654663\n",
            "-- Generation 16 --\n",
            "  Evaluated 193 individuals\n",
            "  Min 74.0\n",
            "  Max 88.0\n",
            "  Avg 82.74666666666667\n",
            "  Std 2.1823127385616807\n",
            "-- Generation 17 --\n",
            "  Evaluated 189 individuals\n",
            "  Min 74.0\n",
            "  Max 90.0\n",
            "  Avg 83.66333333333333\n",
            "  Std 2.54885377288627\n",
            "-- Generation 18 --\n",
            "  Evaluated 190 individuals\n",
            "  Min 76.0\n",
            "  Max 90.0\n",
            "  Avg 84.82333333333334\n",
            "  Std 2.5869136480023567\n",
            "-- Generation 19 --\n",
            "  Evaluated 197 individuals\n",
            "  Min 77.0\n",
            "  Max 91.0\n",
            "  Avg 86.28\n",
            "  Std 2.2850820554194224\n",
            "-- Generation 20 --\n",
            "  Evaluated 176 individuals\n",
            "  Min 78.0\n",
            "  Max 93.0\n",
            "  Avg 87.37666666666667\n",
            "  Std 2.2304234774790266\n",
            "-- Generation 21 --\n",
            "  Evaluated 155 individuals\n",
            "  Min 82.0\n",
            "  Max 93.0\n",
            "  Avg 88.59\n",
            "  Std 1.9566723452499961\n",
            "-- Generation 22 --\n",
            "  Evaluated 195 individuals\n",
            "  Min 79.0\n",
            "  Max 94.0\n",
            "  Avg 89.14\n",
            "  Std 2.3791595154593277\n",
            "-- Generation 23 --\n",
            "  Evaluated 184 individuals\n",
            "  Min 80.0\n",
            "  Max 95.0\n",
            "  Avg 89.99\n",
            "  Std 2.247198255606498\n",
            "-- Generation 24 --\n",
            "  Evaluated 181 individuals\n",
            "  Min 83.0\n",
            "  Max 95.0\n",
            "  Avg 90.8\n",
            "  Std 2.2030282189146777\n",
            "-- Generation 25 --\n",
            "  Evaluated 184 individuals\n",
            "  Min 83.0\n",
            "  Max 95.0\n",
            "  Avg 91.48333333333333\n",
            "  Std 2.28248159296453\n",
            "-- Generation 26 --\n",
            "  Evaluated 171 individuals\n",
            "  Min 80.0\n",
            "  Max 97.0\n",
            "  Avg 92.27\n",
            "  Std 2.2884711053452875\n",
            "-- Generation 27 --\n",
            "  Evaluated 167 individuals\n",
            "  Min 82.0\n",
            "  Max 97.0\n",
            "  Avg 93.28666666666666\n",
            "  Std 2.4064819873742134\n",
            "-- Generation 28 --\n",
            "  Evaluated 180 individuals\n",
            "  Min 84.0\n",
            "  Max 98.0\n",
            "  Avg 94.08\n",
            "  Std 2.6820887382785297\n",
            "-- Generation 29 --\n",
            "  Evaluated 179 individuals\n",
            "  Min 85.0\n",
            "  Max 99.0\n",
            "  Avg 95.23\n",
            "  Std 2.0745521605074138\n",
            "-- Generation 30 --\n",
            "  Evaluated 172 individuals\n",
            "  Min 86.0\n",
            "  Max 99.0\n",
            "  Avg 95.80666666666667\n",
            "  Std 2.2692044616754776\n",
            "-- Generation 31 --\n",
            "  Evaluated 151 individuals\n",
            "  Min 85.0\n",
            "  Max 100.0\n",
            "  Avg 96.47\n",
            "  Std 2.348566938936877\n",
            "-- End of (successful) evolution --\n",
            "Best individual is [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], (100.0,)\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "GOnlxzIGVX0Q",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "172d093c-5fd4-40dc-b47e-2d499069bf63"
      },
      "source": [
        "import random\n",
        "\n",
        "from deap import base\n",
        "from deap import creator\n",
        "from deap import tools\n",
        "\n",
        "creator.create(\"FitnessMax\", base.Fitness, weights=(1.0,))\n",
        "creator.create(\"Individual\", list, fitness=creator.FitnessMax)\n",
        "\n",
        "toolbox = base.Toolbox()\n",
        "\n",
        "toolbox.register(\"attr_bool\", random.randint, 0, 1)\n",
        "toolbox.register(\"individual\", tools.initRepeat, creator.Individual, \n",
        "    toolbox.attr_bool, 100)\n",
        "toolbox.register(\"population\", tools.initRepeat, list, toolbox.individual)\n",
        "\n",
        "\n",
        "def evalOneMax(individual):\n",
        "    return sum(individual),\n",
        "\n",
        "\n",
        "toolbox.register(\"evaluate\", evalOneMax)\n",
        "toolbox.register(\"mate\", tools.cxTwoPoint)\n",
        "toolbox.register(\"mutate\", tools.mutFlipBit, indpb=0.05)\n",
        "toolbox.register(\"select\", tools.selTournament, tournsize=3)\n",
        "\n",
        "\n",
        "\n",
        "def main():\n",
        "    random.seed(64)\n",
        "\n",
        "    pop = toolbox.population(n=300)\n",
        "\n",
        "    CXPB, MUTPB = 0.5, 0.2\n",
        "\n",
        "    print(\"Start of evolution\")\n",
        "\n",
        "\n",
        "    fitnesses = list(map(toolbox.evaluate, pop))\n",
        "    for ind, fit in zip(pop, fitnesses):\n",
        "        ind.fitness.values = fit\n",
        "\n",
        "    print(\"  Evaluated %i individuals\" % len(pop))\n",
        "\n",
        "    fits = [ind.fitness.values[0] for ind in pop]\n",
        "\n",
        "    g = 0\n",
        "\n",
        "    while max(fits) < 100 and g < 1000:\n",
        "        g = g + 1\n",
        "        print(\"-- Generation %i --\" % g)\n",
        "\n",
        "        offspring = toolbox.select(pop, len(pop))\n",
        "        offspring = list(map(toolbox.clone, offspring))\n",
        "\n",
        "        for child1, child2 in zip(offspring[::2], offspring[1::2]):\n",
        "\n",
        "            if random.random() < CXPB:\n",
        "                toolbox.mate(child1, child2)\n",
        "\n",
        "                del child1.fitness.values\n",
        "                del child2.fitness.values\n",
        "\n",
        "        for mutant in offspring:\n",
        "\n",
        "            if random.random() < MUTPB:\n",
        "                toolbox.mutate(mutant)\n",
        "                del mutant.fitness.values\n",
        "\n",
        "        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]\n",
        "        fitnesses = map(toolbox.evaluate, invalid_ind)\n",
        "        for ind, fit in zip(invalid_ind, fitnesses):\n",
        "            ind.fitness.values = fit\n",
        "\n",
        "        print(\"  Evaluated %i individuals\" % len(invalid_ind))\n",
        "\n",
        "        pop[:] = offspring\n",
        "\n",
        "        fits = [ind.fitness.values[0] for ind in pop]\n",
        "\n",
        "        length = len(pop)\n",
        "        mean = sum(fits) / length\n",
        "        sum2 = sum(x*x for x in fits)\n",
        "        std = abs(sum2 / length - mean**2)**0.5\n",
        "\n",
        "        print(\"  Min %s\" % min(fits))\n",
        "        print(\"  Max %s\" % max(fits))\n",
        "        print(\"  Avg %s\" % mean)\n",
        "        print(\"  Std %s\" % std)\n",
        "\n",
        "    print(\"-- End of (successful) evolution --\")\n",
        "\n",
        "    best_ind = tools.selBest(pop, 1)[0]\n",
        "    print(\"Best individual is %s, %s\" % (best_ind, best_ind.fitness.values))\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    main()"
      ],
      "execution_count": 40,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "/usr/local/lib/python3.7/dist-packages/deap/creator.py:141: RuntimeWarning: A class named 'FitnessMax' has already been created and it will be overwritten. Consider deleting previous creation of that class or rename it.\n",
            "  RuntimeWarning)\n",
            "/usr/local/lib/python3.7/dist-packages/deap/creator.py:141: RuntimeWarning: A class named 'Individual' has already been created and it will be overwritten. Consider deleting previous creation of that class or rename it.\n",
            "  RuntimeWarning)\n"
          ],
          "name": "stderr"
        },
        {
          "output_type": "stream",
          "text": [
            "Start of evolution\n",
            "  Evaluated 300 individuals\n",
            "-- Generation 1 --\n",
            "  Evaluated 181 individuals\n",
            "  Min 44.0\n",
            "  Max 66.0\n",
            "  Avg 54.833333333333336\n",
            "  Std 4.349584909952722\n",
            "-- Generation 2 --\n",
            "  Evaluated 191 individuals\n",
            "  Min 47.0\n",
            "  Max 68.0\n",
            "  Avg 58.45666666666666\n",
            "  Std 3.455641120769904\n",
            "-- Generation 3 --\n",
            "  Evaluated 199 individuals\n",
            "  Min 52.0\n",
            "  Max 68.0\n",
            "  Avg 60.95333333333333\n",
            "  Std 2.9024970092816367\n",
            "-- Generation 4 --\n",
            "  Evaluated 167 individuals\n",
            "  Min 47.0\n",
            "  Max 71.0\n",
            "  Avg 62.96\n",
            "  Std 2.907186497858939\n",
            "-- Generation 5 --\n",
            "  Evaluated 175 individuals\n",
            "  Min 57.0\n",
            "  Max 73.0\n",
            "  Avg 64.99\n",
            "  Std 2.8489588741621903\n",
            "-- Generation 6 --\n",
            "  Evaluated 168 individuals\n",
            "  Min 58.0\n",
            "  Max 74.0\n",
            "  Avg 66.93333333333334\n",
            "  Std 2.8051539866624524\n",
            "-- Generation 7 --\n",
            "  Evaluated 187 individuals\n",
            "  Min 59.0\n",
            "  Max 76.0\n",
            "  Avg 68.91666666666667\n",
            "  Std 2.826609669236565\n",
            "-- Generation 8 --\n",
            "  Evaluated 171 individuals\n",
            "  Min 62.0\n",
            "  Max 76.0\n",
            "  Avg 70.88666666666667\n",
            "  Std 2.4455038108513407\n",
            "-- Generation 9 --\n",
            "  Evaluated 155 individuals\n",
            "  Min 62.0\n",
            "  Max 80.0\n",
            "  Avg 72.69\n",
            "  Std 2.6243538887379163\n",
            "-- Generation 10 --\n",
            "  Evaluated 171 individuals\n",
            "  Min 64.0\n",
            "  Max 82.0\n",
            "  Avg 74.12333333333333\n",
            "  Std 2.6105150619921655\n",
            "-- Generation 11 --\n",
            "  Evaluated 191 individuals\n",
            "  Min 65.0\n",
            "  Max 82.0\n",
            "  Avg 75.64\n",
            "  Std 2.7000740730579715\n",
            "-- Generation 12 --\n",
            "  Evaluated 171 individuals\n",
            "  Min 69.0\n",
            "  Max 84.0\n",
            "  Avg 77.18\n",
            "  Std 2.5575248451054877\n",
            "-- Generation 13 --\n",
            "  Evaluated 173 individuals\n",
            "  Min 69.0\n",
            "  Max 84.0\n",
            "  Avg 78.76666666666667\n",
            "  Std 2.244746954311161\n",
            "-- Generation 14 --\n",
            "  Evaluated 185 individuals\n",
            "  Min 72.0\n",
            "  Max 86.0\n",
            "  Avg 79.90666666666667\n",
            "  Std 2.3645906387552182\n",
            "-- Generation 15 --\n",
            "  Evaluated 205 individuals\n",
            "  Min 72.0\n",
            "  Max 88.0\n",
            "  Avg 81.44333333333333\n",
            "  Std 2.3805018145108905\n",
            "-- Generation 16 --\n",
            "  Evaluated 163 individuals\n",
            "  Min 74.0\n",
            "  Max 88.0\n",
            "  Avg 82.67666666666666\n",
            "  Std 2.2253364289973994\n",
            "-- Generation 17 --\n",
            "  Evaluated 175 individuals\n",
            "  Min 76.0\n",
            "  Max 88.0\n",
            "  Avg 83.68333333333334\n",
            "  Std 2.3741080196335167\n",
            "-- Generation 18 --\n",
            "  Evaluated 181 individuals\n",
            "  Min 74.0\n",
            "  Max 90.0\n",
            "  Avg 84.80666666666667\n",
            "  Std 2.3027423264928153\n",
            "-- Generation 19 --\n",
            "  Evaluated 179 individuals\n",
            "  Min 74.0\n",
            "  Max 91.0\n",
            "  Avg 85.62333333333333\n",
            "  Std 2.5195480194316042\n",
            "-- Generation 20 --\n",
            "  Evaluated 178 individuals\n",
            "  Min 78.0\n",
            "  Max 91.0\n",
            "  Avg 86.58\n",
            "  Std 2.1641626556246405\n",
            "-- Generation 21 --\n",
            "  Evaluated 173 individuals\n",
            "  Min 78.0\n",
            "  Max 91.0\n",
            "  Avg 87.25333333333333\n",
            "  Std 2.3314849821996857\n",
            "-- Generation 22 --\n",
            "  Evaluated 155 individuals\n",
            "  Min 79.0\n",
            "  Max 92.0\n",
            "  Avg 88.06\n",
            "  Std 2.157869319490837\n",
            "-- Generation 23 --\n",
            "  Evaluated 187 individuals\n",
            "  Min 80.0\n",
            "  Max 92.0\n",
            "  Avg 88.37\n",
            "  Std 2.201461635671229\n",
            "-- Generation 24 --\n",
            "  Evaluated 184 individuals\n",
            "  Min 82.0\n",
            "  Max 94.0\n",
            "  Avg 89.27666666666667\n",
            "  Std 1.9782455751384154\n",
            "-- Generation 25 --\n",
            "  Evaluated 198 individuals\n",
            "  Min 80.0\n",
            "  Max 95.0\n",
            "  Avg 89.77666666666667\n",
            "  Std 2.380501814510508\n",
            "-- Generation 26 --\n",
            "  Evaluated 185 individuals\n",
            "  Min 80.0\n",
            "  Max 96.0\n",
            "  Avg 90.62333333333333\n",
            "  Std 2.415530767531084\n",
            "-- Generation 27 --\n",
            "  Evaluated 160 individuals\n",
            "  Min 82.0\n",
            "  Max 96.0\n",
            "  Avg 91.62\n",
            "  Std 2.252909230306073\n",
            "-- Generation 28 --\n",
            "  Evaluated 182 individuals\n",
            "  Min 83.0\n",
            "  Max 97.0\n",
            "  Avg 92.45\n",
            "  Std 2.3637893307144857\n",
            "-- Generation 29 --\n",
            "  Evaluated 171 individuals\n",
            "  Min 84.0\n",
            "  Max 97.0\n",
            "  Avg 93.29333333333334\n",
            "  Std 2.4658917701760132\n",
            "-- Generation 30 --\n",
            "  Evaluated 184 individuals\n",
            "  Min 84.0\n",
            "  Max 97.0\n",
            "  Avg 94.14333333333333\n",
            "  Std 2.399191993614305\n",
            "-- Generation 31 --\n",
            "  Evaluated 161 individuals\n",
            "  Min 85.0\n",
            "  Max 98.0\n",
            "  Avg 94.91\n",
            "  Std 2.4059440281660702\n",
            "-- Generation 32 --\n",
            "  Evaluated 181 individuals\n",
            "  Min 85.0\n",
            "  Max 99.0\n",
            "  Avg 95.46333333333334\n",
            "  Std 2.2895390123094943\n",
            "-- Generation 33 --\n",
            "  Evaluated 177 individuals\n",
            "  Min 88.0\n",
            "  Max 99.0\n",
            "  Avg 96.02\n",
            "  Std 2.409619610367642\n",
            "-- Generation 34 --\n",
            "  Evaluated 182 individuals\n",
            "  Min 88.0\n",
            "  Max 99.0\n",
            "  Avg 96.77333333333333\n",
            "  Std 2.0917191228485437\n",
            "-- Generation 35 --\n",
            "  Evaluated 177 individuals\n",
            "  Min 86.0\n",
            "  Max 100.0\n",
            "  Avg 97.04333333333334\n",
            "  Std 2.325536975028139\n",
            "-- End of (successful) evolution --\n",
            "Best individual is [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], (100.0,)\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "TKbfeLixqmTa"
      },
      "source": [
        ""
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}