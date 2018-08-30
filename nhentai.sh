#!/bin/bash

# if you encouter problem like: '$\r is not defined'
# run `dos2unix cool.sh`` first


# $1，可选项，一般为 --data_dir 后面接 $2 添加欲创建的目录名。
# $3 也是可选项，一般为 --search 后面接 $4 为 希望搜索的关键词，多个关键词可以用 + 符号连接
# 注意，关键词和 + 之间不要有空格，关键词在一个或两个之间，不推荐太多个关键词
# 示例：`bash setup.sh --data_dir nico_robin --search nico+robin`

python3 nora-higuma.py $1 $2 $3 $4

if [[ $1 == '--data_dir' ]]
then
    new_dir_name="${2:-manga}"
    cd ${new_dir_name}
elif [[ $1 == '--search' ]]
then
    if [[ $3 == '--data_dir' ]]
    then
        new_dir_name="${4:-manga}"
        cd ${new_dir_name}
    elif [[ ! $3 ]]
    then
        new_dir_name="${2:-manga}"
        cd ${new_dir_name}
    fi
elif [[ ! $1 ]]
then
    new_dir_name="manga"
    cd ${new_dir_name}
fi

num=$(ls -l|grep "^d"| wc -l)

for ((a=1; a<(${num}+1); a++)); do
    name=$(echo "$a-$a.txt")
    title=$(cat $name)
    cd ${a}
    aria2c -x2 -i link.txt > /dev/null
    cd ..
    mv "${a}" "${title}"
    rm "$a-$a.txt"
done