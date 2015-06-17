
public class Machine implements EventHandler {
	private double MTTF;
	private double MTTFvariance;
	public boolean working;
	
	public Machine() {
		MTTF = 30.0;
		MTTFvariance = 5.0;
		working = true;
	}
	
	@Override
	public void respondToEvent(Event e, Simulation s) {
		if (e.getType()==s.working) {
                    System.out.println(e.getTime()+" machine working");
                    working=true;

                    double timeToNextFailure =0;

                    if(s.simulation_type==1){
                        timeToNextFailure = Math.abs(s.generator.nextGaussian()*MTTFvariance+MTTF);
                        e.setTime(s.now+timeToNextFailure);
                    }else{
                        timeToNextFailure = s.getNextTimeTrace();
                        e.setTime(timeToNextFailure);
                    }

                    e.setType(s.failure);
                    s.scheduleEvent(e);
                    return;
		}
		if (e.getType()==s.failure) {
                    System.out.println(e.getTime()+" machine failure");
                    working=false;
                    e.setTime(s.now);
                    e.setHandler(s.r);
                    e.setType(s.startRepair);
                    s.scheduleEvent(e);
                    return;
		}

	}

}
