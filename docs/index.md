## Done
_Josias, 31.08.2021_

It is done. Feel free to download the final paper here:

[09_Publication/210831_HSA_Josias-Bruderer_Vom-BBS-zur-Declaration-of-the-Independence-of-Cyberspace.pdf](https://github.com/josiasbruderer/bbs-for-independence/raw/main/09_publication/210831_HSA_Josias-Bruderer_Vom-BBS-zur-Declaration-of-the-Independence-of-Cyberspace.pdf){:target="_blank"}

<img src="https://raw.githubusercontent.com/josiasbruderer/bbs-for-independence/main/docs/assets/images/done.webp">

## Endgame
_Josias, 30.08.2021_

The endgame started - almost everything is ready. The three things that needs to be done is: writing the conclusion, correct typos and attach stuff. There's not much more to say, but more to work. Bye :)  

## Managed to upload states
_Josias, 30.08.2021_

After some fighting with python code, textfiles - a huge amount of, git-stuff and computational power I managed to find a good set of parameters to shrink the dataset to a selection of files that are possible to analyse. And the results are provided in [03_workspace/states](https://github.com/josiasbruderer/bbs-for-independence/tree/main/03_workspace/states){:target="_blank"}. One analysis was run on the declaration and some additional files that mirror the spirit of the declaration quite well, the second analysis was run on all selected categories with filtering applied.

In a nutshell the recieved data tells to things:

1\. The evolution of bbs mirrors inside the textfiles:

![docs per year](/assets/images/docs_per_year.png)

2\. The textfiles are about technology (Octis LDA Topic Model 0):

![Wordcloud LDA Topic 0](/assets/images/wc01.png)

3\. The (early) internet is (and was) for porn (Octis LDA Topic Model 6):

![Wordcloud LDA Topic 6](/assets/images/wc02.png)

<iframe width="480" height="280" src="https://www.youtube.com/embed/LTJvdGcb7Fs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## The Power of R
_Josias, 28.08.2021_

I faced a new challenge: I was aware already that i will need to implement some way of filtering and I had an rough idea how to do it. The difficult part was to find out the categories and parameter that were suited. I got an anwer using R (of course I could have done it with Python but I knew how to handle data with R, so why not using R this time...). I realized that charratioB will be the best choice, so I checked which categories to filter:

![charratioB](/assets/images/charratioB_01.png)

The categories: tap, floppies, exhibits, artifacts, piracy, art, fidonet-on-the-interne will be filtered. This reduces the total of 102'971 files to 44'832.

And the second thing was to find a good value to filter charratioB - I'm still not sure really if 0.95 is a good choice but that's at least what my server should be able to process: 7'241 files could be possible to work with.

![charratioB](/assets/images/charratioB_02.png)

So long... ;-)

Oh and I forgt: the full report can be found in: [03_workspace/dataset_statistics.html](https://github.com/josiasbruderer/bbs-for-independence/blob/e81a2b07181f2f90eea6bc948fb0c956923698b7/03_workspace/dataset_statistics.html){:target="_blank"}

## Taking Shape
_Josias, 23.08.2021_

The paper is getting its shape: The theoretical part is more or less in a final state and the methodological part is not far from being done. It took quite some time and energy to think through all the stuff and getting into writing. And I have to admit, the research was way to interesting and I collected more information than I could write about... Good thing is that it gave me an Idea of the topic i'd like to write my BA-Paper about.  


## Overviewing the sources
_Josias, 09.08.2021_

While going through the researched sources some first comments were written down. It will help to keep an overview. The comments are highlighted in:

[01_research/Quellen.md](https://github.com/josiasbruderer/bbs-for-independence/commit/f18fd198322d7aa7b67d8a497f8bde0ec1224f35){:target="_blank"}

Some sources focus on web 2.0 and social media in general. This was helpful insofar that a comparison between the functionality of BBS and social media could be made. Also there are sources like the text of Schmidt and Taddicken (2017) about social media, space and time or Weyers chapters about realtime society (2019) that are interesting but quite off-topic. These  will be an excursus at most. 

What really helped were the text about NLP (Bender & Koller 2020; Graham, Milligan & Weingart 2016, Merrill et al. 2021), especially to get an idea what is possible and where the limits of NLP. The chapter of Mützel, Saner and Unternährer (2018) will be important in terms of cleaning up data. And last but not least many sources focus on explaining BBS and how the world around BBS was (Dvorak 1990, Turner 2006), the impact of the declaration (Bennett & Strange 2016, Fassler 2008). 

And to close: Reading the sources for this HSA won't stop me from digging into other articles that pops up. Like [A Field Guide for Nature-Resistant Nerds](https://www.wired.com/story/a-field-guide-for-nature-resistant-nerds-microchips-climate-change/){:target="_blank"}:

> Part of the privilege of being a nerd is that you're able to forget you have a body: You cruise around cyberspace, get a beverage out of the fridge, cruise some more. [...] And after a while you realize that science itself is just an API to nature, a bunch of kludges and observations that work well enough to get the job done. 
(Paul Ford @ Wired, 06.08.2021)

## Ready to (re-)read!
_Josias, 21.07.2021_

The first part of the research is done so far (see the researched sources below). Next step is to (re-)read a lot and get a good overview of the sources, so that the writing of the theoretical part of the paper can start next week.

Fyi: To keep track over the tasks and progress I set up a [timeline](https://github.com/josiasbruderer/bbs-for-independence/projects/1){:target="_blank"}. Feel free to check it out! :-)

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fjosiasbruderer%2Fbbs-for-independence%2Fblob%2Fb209e1294944c90f8ec8d982724d61eb0a8c496a%2F01_research%2FQuellen.md&style=an-old-hope&showBorder=on&showLineNumbers=on&showFileMeta=on&showCopy=on"></script>

## A long way to go...
_Josias, 19.07.2021_

This website serves as a documentation of the work related to the paper _From BBS to the Declaration of the Independence of Cyberspace_. 

The following two documents gives an idea what the paper is about:

- [Exposé](https://github.com/josiasbruderer/bbs-for-independence/blob/main/01_research/2021_Bruderer-Josias_Expose-HSA-v2.pdf){:target="_blank"}
- [Mini-Project: Jason Scotts Favorite 100](https://github.com/josiasbruderer/bbs-for-independence/blob/main/01_research/2021_Bruderer-Josias_jason-scotts-favorite-100_README.pdf){:target="_blank"}

More will follow soon. - Check out [GitHub](https://github.com/josiasbruderer/bbs-for-independence){:target="_blank"} to get the latest updates.
