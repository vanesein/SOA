import java.io.*;
import java.util.ArrayList;
import java.util.Random;


import java.util.*;


public class Simulation {
	public Random generator = new Random(); // random number generator
	public EventHeap h;
	double now;
	
	public Machine m = new Machine();
	public Repairman r = new Repairman();
	public User u = new User();
        
        /*Code added by vanessa*/
        public ArrayList <Double>  start_repair_time = new ArrayList();
        public  ArrayList <Double>  finish_repair_time = new ArrayList ();
        public  ArrayList <Double>  machinefail_time = new ArrayList();
        
        public  ArrayList <Double>  downtime = new ArrayList();
        public  ArrayList <Double>  repair_time = new ArrayList();    
           
        public  ArrayList <Double>  trace_time = new ArrayList(); 
        public ListIterator<Double> it_trace = trace_time.listIterator();
        public int simulation_type = 0; //1:para una lectura estocatisca y 2 para una lectura desde un tracedriven creado
        
	public Simulation() {
		generator = new Random();
		h = new EventHeap(10000);
		now = 0;
	}

	public void scheduleEvent(Event e) {
		h.insert(e);
	}
	
	public void setup() {
		Event machineEvent = new Event();
		machineEvent.setHandler(m);
		machineEvent.setType(working);
                
                if(simulation_type==1)
                    machineEvent.setTime(0);
                else
                    machineEvent.setTime(getTimeTrace(0));
                
		scheduleEvent(machineEvent);
		
		Event userEvent = new Event();
		userEvent.setHandler(u);
		userEvent.setType(userCheck);
                userEvent.setTime(60);
		scheduleEvent(userEvent);
		return;
	}
        
        public double getDownTime(){
            double sum = 0.0;
            int p = 0;
            double sr = 0.0;
            double fr = 0.0;
            double mf = 0.0;

            int [] sizes = {machinefail_time.size(),start_repair_time.size(),finish_repair_time.size()};
            int min = sizes[0];
            int max = 0;
            
            for (int i = 1; i < sizes.length; i++) {
                if (sizes[i] < min) min = sizes[i];
                if (sizes[i] > max) max = sizes[i];
            }
            
            while (max > 0){
                if (p+1 > min && machinefail_time.size()>= min) mf = 0;
                else mf = machinefail_time.get(p);
                
                if (p+1 > min && start_repair_time.size()>= min) sr = 0;
                else sr = start_repair_time.get(p);
                
                if (p+1 > min && finish_repair_time.size()>= min) fr = 0;
                else fr = finish_repair_time.get(p);
                
                double t1 = sr - mf;
                double t2 = fr - sr;
                double t = t2 - t1;
                downtime.add(t);
                max--;
                p++; 
            }   
            for(double a : downtime)
                sum += a;
            return sum/downtime.size();
        }
	
        
        public double getRepairTime(){
            double sum = 0.0;
            int p = 0;
            double sr = 0.0;
            double fr = 0.0;

            int [] sizes = {start_repair_time.size(),finish_repair_time.size()};
            int min = sizes[0];
            int max = 0;
            
            for (int i = 1; i < sizes.length; i++) {
                if (sizes[i] < min) min = sizes[i];
                if (sizes[i] > max) max = sizes[i];
            }
            
            while (max > 0){
                
                if (p+1 > min && start_repair_time.size()>= min) sr = 0;
                else sr = start_repair_time.get(p);
                
                if (p+1 > min && finish_repair_time.size()>= min) fr = 0;
                else fr = finish_repair_time.get(p);
                
                double t = fr - sr;
                //double t1 = t - sr;
                repair_time.add(t);
                max--;
                p++; 
            }
                
            for(double a : repair_time)
                sum += a;
            return sum/repair_time.size();
        }
                
       
       
        public double getTimeTrace(int idx){
           if (it_trace.hasNext()) {
            return trace_time.remove(idx);
           }else return 10000;
       }
       
        public double getNextTimeTrace(){
            try{
                if (it_trace.hasNext()) {
                    return trace_time.remove(it_trace.nextIndex()+1);
                }else return 0.0;
            }catch(Exception e){
                return 10000;
            }
       }
 
        public void createTraceDriven(){
            ArrayList <Double>  generated = new ArrayList();
            while (generated.size() < 10000){
                Double next = Math.abs(20 + (10002 - 20) * generator.nextDouble());
                next = now + next;
                generated.add(next);
            }
            Collections.sort(generated);
            try {
                File file = new File("trace_java.txt");
                if (!file.exists()) {
                    file.createNewFile();
                }

                FileWriter fw = new FileWriter(file.getAbsoluteFile());
                BufferedWriter bw = new BufferedWriter(fw);
                Iterator iterator = generated.iterator();

                while (iterator.hasNext()) {
                    bw.write(iterator.next()+"\n");
                }

                bw.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
       
        public void readTrace(){
           try {
                FileReader fileReader = new FileReader("trace_java.txt");
                BufferedReader br = new BufferedReader(fileReader);
                String line = null;

                while((line = br.readLine()) != null) {
                    trace_time.add(Double.parseDouble(line));
                }
                br.close();
            } catch (IOException e) {
            
            }
       }
    
        
        public void run(double maxTime) {
             while (!h.isEmpty() && h.peek().getTime()<=maxTime) {
                Event nextEvent = h.remove();
                now = nextEvent.getTime();
                
                if(nextEvent.getType()==failure){
                    machinefail_time.add(now);
                }    
                if(nextEvent.getType()==startRepair){
                    start_repair_time.add(now);
                }
                if(nextEvent.getType()==finishRepair){
                    finish_repair_time.add(now);
                }

                nextEvent.getHandler().respondToEvent(nextEvent, this);       
            }
            System.out.println("Machine downtime: "+ getDownTime());
            System.out.println("Machine repair time: "+ getRepairTime());
	}
	// events
	public final int working = 1;
	public final int failure = 2;
	public final int startRepair = 3;
	public final int finishRepair = 4;
	public final int userCheck = 5;

}
