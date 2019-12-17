mu=0
sigma=0
nb_play=1
units=1
__units__=256
points=1000
activation=tanh
method=sin
input_dim=1
state=0
lr=0.001

for nb_plays in 1 50 100 500
do
    units=$nb_plays
    if [[ $nb_plays == 500 ]]; then
        units=100
    fi

    for __units__ in 1 8 16 32 64 128 256
    do
        fname="./log/lstm-activation-${activation}-lr-${lr}-mu-${mu}-sigma-${sigma}-nb_play-${nb_plays}-units-${units}-__units__-${__units__}-points-${points}.log"
        log_fname="./new-dataset/lstm/method-${method}/activation-${activation}/state-${state}/input_dim-${input_dim}/mu-${mu}/sigma-${sigma}/units-${units}/nb_plays-${nb_plays}/points-${points}/units#-${__units__}/mse-loss-lr-${lr}.csv"

        cat $fname | grep "loss:" | awk '{print $9}' &> $log_fname
    done
done
