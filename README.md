# True Random Number Generator
## Based on Non-Recurring Improved Random Number Generator - a new step to improve cryptographic algorithms
>Implementation of DOI: [10.4108/eai.12-6-2018.154813][DOI] article in Python 3.9.

The quality of the generated numbers depends mainly on the video file. Ideally, it should be as dynamic as possible. The generator generates a million numbers in a maximum of 10 seconds (depending on your CPU, of course)

Numbers are saved as raw binary so a million 8-bit numbers will take up exactly 1MB
##### Executing:

```python main.py --new [range of numbers]```

```python main.py --append [range of numbers]```

```python main.py --hist```

###Notes
>The generator output file is called *binaryout.bin*, it is created in the main folder. Diehard tests also use it.

## Histogram of generated 1M 8bit numbers
![Histogram](https://raw.githubusercontent.com/D4VOS/true_random_number_generator/97ca73ea80bde7f8fc6bd10ca817d517cb36c1ab/charts/output_m_257.png)

------------
# Diehard tests
> All tests need at least 38 million 32-bit numbers = 152 million 8-bit numbers.
> [All tests are described here][Diehard]
> 
> 
> The implementation of each of the tests is carried out by the Kolmogorov-Smirnov test with a uniform distribution in the range from 0 to 1 of the obtained p_value of each unit test.
###Implemented
- Count-the-1's test
- Parking Lot test
- Squeeze test

### Executing:
```python main.py --test```

------------
###Who knows, he knows
>Jeślli szukasz kodu na BST to chociaż daj gwiazdkę :smile:

[Diehard]:<https://en.wikipedia.org/wiki/Diehard_tests>
[DOI]:<https://www.researchgate.net/publication/325740094_Non-Recurring_Improved_Random_Number_Generator-_a_new_step_to_improve_cryptographic_algorithms/fulltext/5b211af50f7e9b0e3740174d/Non-Recurring-Improved-Random-Number-Generator-a-new-step-to-improve-cryptographic-algorithms.pdf>