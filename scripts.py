from multiprocessing import Process

def script1():
  while True:
    import aws_pubsub_readings

def script2():
  while True:
    import aws_pubsub_status

def script3():
  while True:
    import aws_pubsub_tests

if __name__ == '__main__':
  print ('Running scripts...')

  # proc1 = Process(target = script1)
  # proc1.start()
  # print ('Reading script running...')
  #
  # proc2 = Process(target = script2)
  # proc2.start()
  # print ('Status script running...')

  proc3 = Process(target=script3)
  proc3.start()
  print('Status script running...')

  print ('Scripts running')