import numpy as np
import torch as tr
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt


AVG_UTIL = 6.88461538461539


def estimate_score(blast_point, estimate_util):
    if estimate_util > blast_point:  # blast
        return 0
    # closer to blast, get higher point
    return estimate_util / blast_point * 100  # *100 make loss larger


# data format (e.g,dealer)
# input:  dealer._point, player._point, dealer._action, dealer._blast_point, is_dealer
# output: estimate score (utility), higher when closer to dealer._blast_point, 0 when exceed dealer._blast_point
def create_nn_data(blast_point):
    inp, out = [], []

    # generate data for all case from 1 point to blast point
    for dealer_point in range(1, blast_point+1):
        for player_point in range(1, blast_point+1):
            for action in [1, 0]:
                for is_dealer in [1, 0]:
                    cur_inp = [dealer_point, player_point, action, blast_point, is_dealer]
                    inp.append(cur_inp)
                    # 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A(1/10) AVG_UTIL=6.88461538461539
                    # hit util = 6.8846, stop util = 0
                    if action:
                        estimate_util = dealer_point + AVG_UTIL if is_dealer else player_point + AVG_UTIL
                        score = estimate_score(blast_point, estimate_util)
                        out.append(score)
                    else:
                        estimate_util = dealer_point if is_dealer else player_point
                        score = estimate_score(blast_point, estimate_util)
                        out.append(score)
    return inp*25, out*25


def train(dataloader, model, loss_fn, optimizer):
    # model(input) returns output
    # loss_fn(output, target) returns loss
    # standard torch dataloader and optimizer

    # total number of examples for progress updates
    num_examples = len(dataloader.dataset)

    # use the model in training mode
    model.train()

    loss_list = []

    # loop over every batch in the dataset
    for batch, (inp, targ) in enumerate(dataloader):

        # Put the data on the device (gpu if available else cpu)
        inp, targ = inp.to(device), targ.to(device)

        # Compute prediction error
        out = model(inp)
        loss = loss_fn(out, targ)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Progress update
        if batch % 10 == 0:
            loss, current = loss.item(), batch * len(inp)
            loss_list.append(np.float(loss))
            print(f"loss: {loss:>7f} [{current:>5d}/{num_examples:>5d}]")
    return loss_list


def test(dataloader, model, loss_fn):
    # number of examples and batches for normalization
    num_examples = len(dataloader.dataset)
    num_batches = len(dataloader)

    # use the model in evaluation mode
    model.eval()

    loss_list = []

    # aggregate test loss and accuracy over dataset
    loss, accuracy = 0, 0
    with tr.no_grad(): # more efficient when gradients are not needed
        for inp, targ in dataloader:
            inp, targ = inp.to(device), targ.to(device)
            out = model(inp)
            ll = loss_fn(out, targ).item()
            loss += ll
            loss_list.append(np.float(ll))
            accuracy += (out.argmax(dim=1) == targ).sum().item()
    loss /= num_batches
    accuracy /= num_examples
    print(f"Test Error: \n Accuracy: {(100*accuracy):>0.1f}%, Avg loss: {loss:>8f} \n")
    return loss_list


# run training for several epochs (passes over the dataset)
def do_epochs(train_dataloader, test_dataloader, model, loss_fn, optimizer):
    epochs = 3
    train_loss_list, test_loss_list = [], []
    for t in range(epochs):
        print(f"Epoch {t + 1}\n-------------------------------")
        train_loss = train(train_dataloader, model, loss_fn, optimizer)
        test_loss = test(test_dataloader, model, loss_fn)
        train_loss_list.extend(train_loss)
        test_loss_list.extend(test_loss)
    print("Done!")
    return train_loss_list, test_loss_list


# Use a GPU device if available
device = "cuda" if tr.cuda.is_available() else "cpu"
print(f"Using {device} device")

cnn = tr.nn.Sequential(
    tr.nn.Linear(5, 10),  # Fully connected layer with 5 input units and 10 output units
    tr.nn.ReLU(),  # ReLU activation layer
    tr.nn.Flatten(),
    tr.nn.Linear(10, 1)  # Fully connected layer with 10 input units and 1 output unit
).to(device)
cnn2 = tr.nn.Sequential(
    tr.nn.Linear(5, 10),  # Fully connected layer with 5 input units and 10 output units
    tr.nn.ELU(),  # ReLU activation layer
    tr.nn.Flatten(),
    tr.nn.Linear(10, 1)  # Fully connected layer with 10 input units and 1 output unit
).to(device)


if __name__ == '__main__':
    #loss_fn = tr.nn.CrossEntropyLoss()
    loss_fn = tr.nn.L1Loss()
    optimizer = tr.optim.SGD(cnn.parameters(), lr=1e-1)

    # generate data
    inp, out = create_nn_data(blast_point=21)
    inp_tr, out_tr = tr.tensor(inp, dtype=tr.float), tr.tensor(out, dtype=tr.float)
    dataset = TensorDataset(inp_tr, out_tr)
    train_size = int(0.9 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = tr.utils.data.random_split(dataset, [train_size, test_size])
    train_dataloader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=64, shuffle=True)

    train_loss_list, test_loss_list = do_epochs(train_dataloader, test_dataloader, cnn, loss_fn, optimizer)
    #train_loss_list, test_loss_list = do_epochs(train_dataloader, test_dataloader, cnn2, loss_fn, optimizer)

    tr.save(cnn.state_dict(), 'model/CNN.pkl')
    #tr.save(cnn.state_dict(), 'model/CNN2.pkl')

    # Training and Testing Error
    plt.figure()
    plt.grid()
    slice = min(len(train_loss_list), len(test_loss_list))
    plt.plot([i for i in range(len(train_loss_list[:slice]))], train_loss_list[:slice], label='Train Loss')
    plt.plot([i for i in range(len(test_loss_list[:slice]))], test_loss_list[:slice], label='Test Loss')
    plt.legend()
    plt.title("Training and Testing Error")
    plt.xlabel("Number of Test")
    plt.ylabel("Error")
    plt.savefig("res/Training and Testing Error")
    plt.show()


