# From BBS to the Declaration of the Independence of Cyberspace

This repository will store all files related to the term paper _from BBS to the Declaration of the Independence of Cyberspace_ related to the course _[The ABC of Computational Text Analysis](https://aflueckiger.github.io/KED2021/)_.

## Repository File Structure

* 01_research: contains papers, publications, docs and notes that were researched
* 02_datasets: contains raw datasets that will be analyzed;
* 03_workspace: contains jupyter notebooks, python code and is the place where the magical things happens
* 04_paper: contains the markdown and latex files for the final paper
* 09_publication: contains the file(s) that will be handed in / published in the end
* docs: contains the github pages file that will act like a journal to document the working progress. It can be accessed under [https://josiasbruderer.github.io/bbs-for-independence/](https://josiasbruderer.github.io/bbs-for-independence/).

## Useful Commands

Here are some commands that will help to navigate through the repo and _get things running._

```bash
#install git-lfs and fetch files
pamac install git-lfs
cd bbs-for-independence
git lfs intall
git lfs fetch
git lfs pull

#serve github pages locally
cd docs
bundle exec jekyll serve

#start junyper lab
cd 03_workspace
./start-jupyter.sh

#install requirements
sudo pip install -r requirements.txt

#run main script
# run before first time: python3 -m spacy download en_core_web_sm
python3 ./03_workspace/main.py

#use OCTIS dashboard
cd 03_workspace
git clone https://github.com/MIND-Lab/OCTIS.git
cd OCTIS
pip install octis
python setup.py
python octis/dashboard/server.py

```